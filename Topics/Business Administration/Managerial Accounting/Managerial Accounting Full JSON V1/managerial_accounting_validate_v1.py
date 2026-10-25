#!/usr/bin/env python3
"""Validate this reasoning package; run explicit synthetic models, never formula strings.

Python 3.10+; standard library only. No network, spreadsheet engine or external packages.
Default invocation prints a report without changing packaged files. Use --report explicitly
for a new report (doing so invalidates a pre-existing checksum manifest for that report).
"""
from __future__ import annotations
import argparse
from collections import Counter
from datetime import date, datetime, timezone
import hashlib
import json
import math
from pathlib import Path
import sys
import zipfile
import xml.etree.ElementTree as ET
from typing import Any, Callable

FILES = [
 'hilton_platt_managerial_accounting_reasoning_v1.json',
 'managerial_accounting_source_map_v1.json',
 'managerial_accounting_model_tests_v1.json',
 'managerial_accounting_assistant_context_v1.json',
 'MANAGERIAL_ACCOUNTING_START_HERE_v1.md',
 'managerial_accounting_validate_v1.py',
 'managerial_accounting_validation_report_v1.json',
 'managerial_accounting_file_index_v1.json',
 'managerial_accounting_checksums_v1.sha256.json']
STATUSES={'passed','failed','not_run','blocked','requires_human_review'}
LAYERS={'textbook_explanation','analytical_derivation','application_extension','project_evidence','current_external_verification'}
BASES={'source_statement','source_example','synthesis','analytical_derivation','application_extension','verified_external_material'}
FAMILIES={'concept','model','decision','risk','workflow','application','route'}
TYPES={'number','integer','number_array','integer_array','number_matrix','date','dated_cash_flow_array'}
TOL=1e-9

class ModelError(ValueError):
    def __init__(self,code: str,message: str):
        self.code=code
        super().__init__(message)

def require(condition: bool, code: str, message: str) -> None:
    if not condition: raise ModelError(code,message)

def num(x: Any) -> bool:
    return not isinstance(x,bool) and isinstance(x,(int,float)) and math.isfinite(x)

def positive(x: float,name: str) -> None:
    require(x>0,'zero_divisor' if x==0 else 'domain',name+' must be positive')

def equal_arrays(*arrays: list) -> None:
    require(bool(arrays) and len(arrays[0])>0 and all(len(a)==len(arrays[0]) for a in arrays),'dimension','Arrays must be nonempty and equal length')

def nonnegative(values: list, name: str) -> None:
    require(all(v>=0 for v in values),'domain',name+' must be nonnegative')

def proportions(total: float, weights: list[float]) -> list[float]:
    nonnegative(weights,'allocation weights'); positive(sum(weights),'sum of weights')
    return [total*w/sum(weights) for w in weights]

def manufacturing_cost_flow(x):
    dm=x['begin_raw']+x['purchases']-x['end_raw']-x['indirect_material']
    mc=dm+x['direct_labor']+x['applied_overhead'];cg=x['begin_wip']+mc-x['end_wip'];co=x['begin_finished']+cg-x['end_finished']
    require(min(dm,mc,cg,co)>=0,'balance','Inventory/cost inputs imply negative flows outside this model scope')
    return dict(direct_material_used=dm,manufacturing_cost=mc,cost_goods_manufactured=cg,unadjusted_cogs=co)

def job_overhead(x):
    positive(x['budget_driver'],'budget_driver');rate=x['budget_overhead']/x['budget_driver'];ja=rate*x['job_driver'];pa=rate*x['period_actual_driver']
    return dict(overhead_rate=rate,job_applied_overhead=ja,job_cost=x['job_material']+x['job_labor']+ja,period_applied_overhead=pa,underapplied_overhead=x['period_actual_overhead']-pa)

def process_weighted_average(x):
    require(math.isclose(x['begin_units']+x['started_units'],x['completed_units']+x['end_units'],abs_tol=1e-6,rel_tol=1e-9),'balance','Physical units do not reconcile')
    require(0<=x['end_material_completion']<=1 and 0<=x['end_conversion_completion']<=1,'domain','Completion fractions must be between zero and one')
    me=x['completed_units']+x['end_units']*x['end_material_completion'];ce=x['completed_units']+x['end_units']*x['end_conversion_completion'];positive(me,'material equivalent units');positive(ce,'conversion equivalent units')
    m=x['begin_material_cost']+x['added_material_cost'];c=x['begin_conversion_cost']+x['added_conversion_cost'];mr=m/me;cr=c/ce
    tr=x['completed_units']*(mr+cr);en=x['end_units']*(x['end_material_completion']*mr+x['end_conversion_completion']*cr)
    return dict(material_eu=me,conversion_eu=ce,material_unit_cost=mr,conversion_unit_cost=cr,transferred_cost=tr,ending_wip_cost=en,cost_reconciliation=m+c-tr-en)

def abc_pool_allocation(x):
    positive(x['denominator_driver'],'denominator_driver');nonnegative(x['object_driver'],'object_driver')
    r=x['pool_cost']/x['denominator_driver'];a=[r*q for q in x['object_driver']]
    return dict(pool_rate=r,assigned_costs=a,total_assigned=sum(a),unassigned_balance=x['pool_cost']-sum(a))

def tdabc_capacity(x):
    positive(x['practical_minutes'],'practical_minutes');require(x['used_minutes']<=x['practical_minutes'],'domain','Used capacity exceeds practical capacity; revise the capacity model')
    r=x['supplied_resource_cost']/x['practical_minutes'];u=x['practical_minutes']-x['used_minutes']
    return dict(capacity_cost_rate=r,used_resource_cost=x['used_minutes']*r,unused_minutes=u,unused_capacity_cost=u*r)

def high_low(x):
    require(x['high_activity']>x['low_activity'],'domain','High activity must exceed low activity')
    require(x['low_activity']<=x['prediction_activity']<=x['high_activity'],'out_of_range','This implementation withholds extrapolation beyond the observed activity endpoints')
    b=(x['cost_at_high']-x['cost_at_low'])/(x['high_activity']-x['low_activity']);a=x['cost_at_high']-b*x['high_activity']
    return dict(variable_rate=b,fixed_component=a,predicted_cost=a+b*x['prediction_activity'])

def simple_least_squares(x):
    xx=x['activity'];yy=x['cost'];equal_arrays(xx,yy);nonnegative(xx,'activity');nonnegative(yy,'cost');require(len(xx)>=2,'dimension','At least two observations required')
    xm=sum(xx)/len(xx);ym=sum(yy)/len(yy);d=sum((v-xm)**2 for v in xx);positive(d,'activity variation')
    b=sum((a-xm)*(c-ym) for a,c in zip(xx,yy))/d;a=ym-b*xm;sse=sum((c-a-b*v)**2 for v,c in zip(xx,yy));sst=sum((c-ym)**2 for c in yy)
    return dict(mean_activity=xm,mean_cost=ym,slope=b,intercept=a,sse=sse,sst=sst,r_squared=None if sst==0 else 1-sse/sst)

def single_product_cvp(x):
    positive(x['price'],'price');cm=x['price']-x['variable_unit_cost'];f=x['fixed_cost'];t=x['target_profit']
    # Zero fixed cost and negative CM break even only at zero; CM=0,F=0 has no unique threshold.
    be=f/cm if cm>0 else 0.0 if f==0 and cm<0 else None
    target=(f+t)/cm if cm>0 else 0.0 if f+t==0 and cm<0 else None
    return dict(unit_contribution=cm,contribution_ratio=cm/x['price'],profit=cm*x['quantity']-f,break_even_units=be,target_units=target,break_even_sales=None if be is None else be*x['price'])

def sales_mix_cvp(x):
    c=x['unit_contributions'];w=x['unit_mix_weights'];equal_arrays(c,w);require(all(0<=a<=1 for a in w) and math.isclose(sum(w),1,abs_tol=1e-9,rel_tol=0),'domain','Unit sales-mix weights must sum to one')
    cm=sum(a*b for a,b in zip(c,w));be=x['fixed_cost']/cm if cm>0 else 0.0 if cm<0 and x['fixed_cost']==0 else None
    return dict(weighted_unit_contribution=cm,break_even_total_units=be,break_even_product_units=None if be is None else [be*v for v in w])

def operating_leverage(x):
    positive(x['operating_profit'],'operating_profit');require(x['sales_change_fraction']>=-1,'domain','Sales decline cannot exceed 100% in this model')
    d=x['contribution_margin']/x['operating_profit'];p=d*x['sales_change_fraction']
    return dict(leverage_factor=d,profit_change_fraction=p,new_profit=x['operating_profit']*(1+p))

def inventory_profit_reconciliation(x):
    d=x['end_fixed_overhead_inventory']-x['begin_fixed_overhead_inventory'];return dict(income_difference=d,absorption_income=x['variable_income']+d)

def quality_cost_report(x):
    a=[x[k] for k in ('prevention','appraisal','internal_failure','external_failure')];s=sum(a)
    return dict(total_quality_cost=s,category_shares=None if s==0 else [v/s for v in a])

def production_materials_budget(x):
    p=x['sales_units']+x['end_finished_target']-x['begin_finished'];u=p*x['material_per_unit'];q=u+x['end_material_target']-x['begin_material'];require(p>=0 and q>=0,'balance','Negative production or purchases requires a different inventory-disposition model')
    return dict(production_units=p,material_usage=u,material_purchases=q,purchase_cost=q*x['material_price'])

def accrual_cash_rollforward(x):
    ar=x['begin_receivables']+x['recognized_revenue']-x['collections'];ap=x['begin_payables']+x['recognized_expense']-x['payments'];require(ar>=0 and ap>=0,'balance','Receivable/payable balance outside the simplified model scope')
    ch=x['collections']-x['payments'];return dict(profit=x['recognized_revenue']-x['recognized_expense'],end_receivables=ar,end_payables=ap,end_cash=x['begin_cash']+ch,cash_change=ch)

def material_usage_variances(x):
    sq=x['actual_output']*x['standard_input_per_output'];p=x['actual_used']*(x['actual_price']-x['standard_price']);q=x['standard_price']*(x['actual_used']-sq)
    return dict(standard_allowed=sq,price_variance=p,quantity_variance=q,total_variance=x['actual_used']*x['actual_price']-sq*x['standard_price'])

def material_purchase_price(x):
    return dict(purchase_price_variance=x['purchased_quantity']*(x['purchase_price']-x['standard_price']))

def labor_variances(x):
    sh=x['actual_output']*x['standard_hours_per_output'];r=x['actual_hours']*(x['actual_rate']-x['standard_rate']);e=x['standard_rate']*(x['actual_hours']-sh)
    return dict(standard_hours=sh,rate_variance=r,efficiency_variance=e,total_variance=x['actual_hours']*x['actual_rate']-sh*x['standard_rate'])

def flexible_cost_bridge(x):
    s=x['fixed_cost']+x['variable_rate']*x['budget_activity'];f=x['fixed_cost']+x['variable_rate']*x['actual_activity']
    return dict(static_budget=s,flexible_budget=f,activity_component=f-s,spending_component=x['actual_cost']-f,total_difference=x['actual_cost']-s)

def variable_overhead_variances(x):
    p=x['actual_driver']*x['standard_rate'];a=x['allowed_driver']*x['standard_rate'];return dict(projected_overhead=p,applied_overhead=a,spending_variance=x['actual_overhead']-p,efficiency_variance=p-a,total_variance=x['actual_overhead']-a)

def fixed_overhead_variances(x):
    positive(x['denominator_driver'],'denominator_driver');r=x['budget_fixed']/x['denominator_driver'];a=r*x['allowed_driver'];return dict(fixed_rate=r,applied_fixed=a,budget_variance=x['actual_fixed']-x['budget_fixed'],volume_variance=x['budget_fixed']-a,total_underapplied=x['actual_fixed']-a)

def sales_revenue_variances(x):
    return dict(price_variance=x['actual_units']*(x['actual_price']-x['budget_price']),volume_variance=(x['actual_units']-x['budget_units'])*x['budget_price'],revenue_difference=x['actual_units']*x['actual_price']-x['budget_units']*x['budget_price'])

def segmented_contribution(x):
    s=x['segment_sales'];v=x['segment_variable_costs'];f=x['segment_traceable_fixed'];equal_arrays(s,v,f)
    for a in (s,v,f):nonnegative(a,'segment values')
    c=[a-b for a,b in zip(s,v)];m=[a-b for a,b in zip(c,f)];return dict(contributions=c,segment_margins=m,group_income=sum(m)-x['common_fixed'])

def roi_residual_income(x):
    positive(x['sales'],'sales');positive(x['average_investment'],'average_investment');a=x['average_investment'];charge=a*x['required_return']
    return dict(roi=x['income']/a,sales_margin=x['income']/x['sales'],capital_turnover=x['sales']/a,capital_charge=charge,residual_income=x['income']-charge)

def eva_edition(x):
    c=x['average_total_assets']-x['average_current_liabilities'];require(c>=0,'domain','This EVA illustration requires nonnegative assets less current liabilities');charge=c*x['wacc'];return dict(capital_base=c,capital_charge=charge,eva=x['after_tax_operating_income']-charge)

def transfer_economic_floor(x):return dict(economic_transfer_benchmark=x['incremental_outlay_per_unit']+x['opportunity_cost_per_unit'])
def special_order(x):return dict(net_benefit=x['order_units']*(x['order_price']-x['incremental_unit_cost'])-x['incremental_fixed']-x['opportunity_cost'])
def make_or_buy(x):return dict(buy_advantage=x['avoidable_make_cost']+x['freed_capacity_benefit']-x['supplier_total']-x['transition_cost'])
def keep_or_drop(x):return dict(drop_advantage=x['avoidable_variable']+x['avoidable_fixed']+x['alternative_use_benefit']-x['lost_revenue']-x['other_lost_contribution']-x['closure_cost'])
def further_processing(x):return dict(further_processing_benefit=x['sales_after_processing']-x['sales_at_splitoff']-x['separable_cost']-x['opportunity_cost'])

def single_bottleneck_ranking(x):
    c=x['unit_contribution'];q=x['scarce_resource_per_unit'];equal_arrays(c,q)
    for a in q:positive(a,'scarce resource per unit')
    return dict(contribution_per_resource=[a/b for a,b in zip(c,q)])

def cost_plus_target_roi(x):
    positive(x['unit_cost_base'],'unit_cost_base');positive(x['planned_units'],'planned_units');t=x['investment']*x['target_roi'];m=(t+x['excluded_period_cost'])/(x['planned_units']*x['unit_cost_base']);return dict(target_profit=t,markup_fraction=m,price=x['unit_cost_base']*(1+m))
def target_cost(x):return dict(target_unit_cost=x['target_price']-x['target_profit_per_unit'])

def dated_annual_npv(x):
    initial=date.fromisoformat(x['initial_date']);flows=x['cash_flows'];require(len(flows)>0,'dimension','Cash-flow schedule required');require(flows[0]['date']==x['initial_date'],'domain','First cash-flow date must equal initial date')
    require(x['annual_discount_rate']>-1,'domain','Annual discount rate must exceed -1');previous=None;pvs=[]
    for row in flows:
        d=date.fromisoformat(row['date']);require(d>=initial and (previous is None or d>previous),'domain','Dates must be strictly increasing from initial date')
        require((d.month,d.day)==(initial.month,initial.day),'domain','Only exact annual anniversaries supported; no guessed day-count convention')
        pvs.append(row['amount']/(1+x['annual_discount_rate'])**(d.year-initial.year));previous=d
    return dict(present_values=pvs,npv=sum(pvs))

def conventional_irr(x):
    cf=x['cash_flows'];require(len(cf)>=2 and cf[0]<0 and all(a>=0 for a in cf[1:]) and any(a>0 for a in cf[1:]),'unsupported_cash_flow','IRR implementation accepts only a conventional initial outflow followed by nonnegative inflows')
    lo=x['lower_rate'];hi=x['upper_rate'];require(-1<lo<hi,'domain','IRR bracket must be ordered and greater than -1')
    def value(rate):return sum(a/(1+rate)**i for i,a in enumerate(cf))
    vl=value(lo);vh=value(hi);require(vl*vh<=0,'not_bracketed','No root bracketed by supplied rates')
    if vl==0:return dict(irr=lo,npv_at_irr=vl)
    if vh==0:return dict(irr=hi,npv_at_irr=vh)
    # Conventional cash-flow derivative is negative; bisection needs no formula evaluator.
    for _ in range(250):
        mid=(lo+hi)/2;vm=value(mid)
        if abs(vm)<1e-10 or hi-lo<1e-14:return dict(irr=mid,npv_at_irr=vm)
        if vm>0:lo=mid
        else:hi=mid
    raise ModelError('convergence','IRR bisection did not converge')

def after_tax_operating_cash(x):
    require(0<=x['tax_rate']<=1,'domain','Tax rate must be a supplied fraction from zero to one');i=x['cash_revenue']-x['cash_operating_cost']-x['tax_depreciation'];t=i*x['tax_rate'];return dict(taxable_income=i,tax_cash=t,operating_cash_flow=x['cash_revenue']-x['cash_operating_cost']-t)
def payback_level(x):positive(x['annual_after_tax_inflow'],'annual_after_tax_inflow');return dict(payback_years=x['initial_investment']/x['annual_after_tax_inflow'])

def payback_uneven(x):
    a=x['annual_inflows'];nonnegative(a,'annual_inflows');require(len(a)>0,'dimension','Provide a nonempty inflow horizon');running=0;year=0 if x['initial_investment']==0 else None
    for i,v in enumerate(a,1):
        running+=v
        if year is None and running>=x['initial_investment']:year=i
    return dict(payback_year_end=year,unrecovered_amount=max(0,x['initial_investment']-running))

def arr_initial(x):positive(x['initial_investment'],'initial_investment');return dict(accounting_return=x['average_annual_income']/x['initial_investment'])
def arr_average(x):positive(x['average_investment'],'average_investment');return dict(accounting_return=x['average_annual_income']/x['average_investment'])
def profitability_index(x):positive(x['initial_investment'],'initial_investment');return dict(profitability_index=x['pv_future_cash_flows']/x['initial_investment'],npv=x['pv_future_cash_flows']-x['initial_investment'])
def nominal_real_rate(x):require(x['real_rate']>-1 and x['inflation_rate']>-1,'domain','Real and inflation rates must exceed -1');return dict(nominal_rate=(1+x['real_rate'])*(1+x['inflation_rate'])-1)

def service_direct(x):
    c=x['service_costs'];u=x['production_usage'];require(len(c)==len(u) and len(c)>0,'dimension','One usage row per service department required');nonnegative(c,'service_costs');require(len(u[0])>0 and all(len(r)==len(u[0]) for r in u),'dimension','Rectangular nonempty production-usage matrix required')
    rows=[proportions(t,r) for t,r in zip(c,u)];return dict(allocations_by_service=rows,production_totals=[sum(r[j] for r in rows) for j in range(len(u[0]))])

def service_dimensions(x,key):
    n=len(x['service_costs']);p=x['production_count'];u=x[key];require(n>0 and p>0 and len(u)==n and all(len(r)==n+p for r in u),'dimension','Service matrix must have n rows and n+production_count columns');nonnegative(x['service_costs'],'service_costs')
    for i,r in enumerate(u):nonnegative(r,key);require(r[i]==0,'domain','No direct self-service entries in this specification')
    return n,p,u

def service_step_down(x):
    n,p,u=service_dimensions(x,'usage');seq=x['sequence'];require(sorted(seq)==list(range(n)),'dimension','Sequence must be a permutation of service-department indexes');running=x['service_costs'][:];rows=[[0.0]*(n+p) for _ in range(n)];closed=set();prod=[0.0]*p
    for i in seq:
        eligible=[j for j in range(n+p) if j!=i and j not in closed];den=sum(u[i][j] for j in eligible)
        if running[i]!=0:positive(den,'remaining step-down allocation base')
        for j in eligible:
            v=0.0 if den==0 else running[i]*u[i][j]/den;rows[i][j]=v
            if j<n:running[j]+=v
            else:prod[j-n]+=v
        closed.add(i)
    require(math.isclose(sum(prod),sum(x['service_costs']),abs_tol=1e-6,rel_tol=1e-9),'balance','Step-down production allocation failed reconciliation')
    return dict(step_allocations=rows,production_totals=prod)

def solve_linear(matrix,rhs):
    n=len(rhs);a=[list(row)+[value] for row,value in zip(matrix,rhs)]
    for i in range(n):
        pivot=max(range(i,n),key=lambda k:abs(a[k][i]));require(abs(a[pivot][i])>1e-12,'singular','Reciprocal system is singular or near singular');a[i],a[pivot]=a[pivot],a[i];v=a[i][i];a[i]=[z/v for z in a[i]]
        for k in range(n):
            if k!=i:
                factor=a[k][i];a[k]=[u-factor*v for u,v in zip(a[k],a[i])]
    return [r[-1] for r in a]

def service_reciprocal(x):
    n,p,u=service_dimensions(x,'usage_fractions')
    for r in u:require(math.isclose(sum(r),1,abs_tol=1e-9,rel_tol=0),'domain','Each complete service-usage row must sum to one')
    matrix=[[(1.0 if i==j else 0.0)-u[j][i] for j in range(n)] for i in range(n)];t=solve_linear(matrix,x['service_costs']);require(all(v>=-1e-8 for v in t),'domain','Reciprocal solution contains negative service costs')
    prod=[sum(t[i]*u[i][n+j] for i in range(n)) for j in range(p)];res=sum(x['service_costs'])-sum(prod);require(math.isclose(res,0,abs_tol=1e-6,rel_tol=0),'balance','Reciprocal allocations do not reconcile to original support costs')
    return dict(service_total_costs=t,production_totals=prod,reconciliation=res)

def dual_service_allocation(x):
    equal_arrays(x['short_run_usage'],x['long_run_usage']);v=proportions(x['budget_variable_cost'],x['short_run_usage']);f=proportions(x['budget_fixed_cost'],x['long_run_usage']);return dict(variable_allocations=v,fixed_allocations=f,total_allocations=[a+b for a,b in zip(v,f)])
def joint_physical(x):return dict(joint_allocations=proportions(x['joint_cost'],x['physical_units']))
def joint_sales(x):return dict(joint_allocations=proportions(x['joint_cost'],x['splitoff_sales_values']))

def joint_nrv(x):
    f=x['final_sales_values'];s=x['separable_costs'];equal_arrays(f,s);nonnegative(f,'final sales');nonnegative(s,'separable costs');v=[a-b for a,b in zip(f,s)];require(all(a>=0 for a in v),'domain','Negative NRV requires a separately specified treatment');return dict(net_realizable_values=v,joint_allocations=proportions(x['joint_cost'],v))

def single_cash_flow_time_value(x):
    require(x['rate']>-1,'domain','Rate must exceed -1');return dict(future_value=x['principal']*(1+x['rate'])**x['periods'],present_value=x['future_cash_flow']/(1+x['rate'])**x['periods'])

def eoq(x):
    positive(x['cost_per_order'],'cost_per_order');positive(x['annual_holding_per_unit'],'annual_holding_per_unit');d=x['annual_demand'];q=math.sqrt(2*d*x['cost_per_order']/x['annual_holding_per_unit']);o=0 if d==0 else d/q*x['cost_per_order'];h=q*x['annual_holding_per_unit']/2;return dict(eoq=q,annual_ordering_cost=o,annual_holding_cost=h,total_relevant_cost=o+h)
def reorder_point(x):return dict(reorder_point=x['daily_usage']*x['lead_days']+x['safety_stock'])
def percentage_comparison(x):return dict(percentage_point_change=100*(x['new_ratio']-x['old_ratio']),relative_percent_change=None if x['old_ratio']==0 else 100*(x['new_ratio']-x['old_ratio'])/x['old_ratio'])

def weighted_group_ratio(x):
    n=x['numerators'];d=x['denominators'];equal_arrays(n,d);nonnegative(d,'denominators');positive(sum(d),'group denominator');return dict(total_numerator=sum(n),total_denominator=sum(d),group_ratio=sum(n)/sum(d),simple_mean_ratio=None if any(v==0 for v in d) else sum(a/b for a,b in zip(n,d))/len(n))

def food_usage_yield(x):
    require(0<x['yield_fraction']<=1,'domain','Yield fraction must be supplied and within (0,1]');r=x['begin_purchase_units']+x['purchases']+x['net_transfers_in']-x['end_purchase_units'];require(r>=0,'balance','Negative recorded usage requires inventory/transfer reconciliation');t=x['portions']*x['usable_units_per_portion']/x['yield_fraction'];return dict(recorded_usage=r,theoretical_usage=t,unexplained_usage_difference=r-t)

# Fixed allowlist of callables, not eval/exec/imports selected by input data.
IMPLEMENTATIONS={
 'manufacturing_cost_flow':manufacturing_cost_flow,'job_overhead':job_overhead,'process_weighted_average':process_weighted_average,
 'abc_pool_allocation':abc_pool_allocation,'tdabc_capacity':tdabc_capacity,'high_low':high_low,'simple_least_squares':simple_least_squares,
 'single_product_cvp':single_product_cvp,'sales_mix_cvp':sales_mix_cvp,'operating_leverage':operating_leverage,
 'inventory_profit_reconciliation':inventory_profit_reconciliation,'quality_cost_report':quality_cost_report,
 'production_materials_budget':production_materials_budget,'accrual_cash_rollforward':accrual_cash_rollforward,
 'material_usage_variances':material_usage_variances,'material_purchase_price':material_purchase_price,'labor_variances':labor_variances,
 'flexible_cost_bridge':flexible_cost_bridge,'variable_overhead_variances':variable_overhead_variances,'fixed_overhead_variances':fixed_overhead_variances,
 'sales_revenue_variances':sales_revenue_variances,'segmented_contribution':segmented_contribution,'roi_residual_income':roi_residual_income,
 'eva_edition':eva_edition,'transfer_economic_floor':transfer_economic_floor,'special_order':special_order,'make_or_buy':make_or_buy,
 'keep_or_drop':keep_or_drop,'further_processing':further_processing,'single_bottleneck_ranking':single_bottleneck_ranking,
 'cost_plus_target_roi':cost_plus_target_roi,'target_cost':target_cost,'dated_annual_npv':dated_annual_npv,'conventional_irr':conventional_irr,
 'after_tax_operating_cash':after_tax_operating_cash,'payback_level':payback_level,'payback_uneven':payback_uneven,'arr_initial':arr_initial,
 'arr_average':arr_average,'profitability_index':profitability_index,'nominal_real_rate':nominal_real_rate,'service_direct':service_direct,
 'service_step_down':service_step_down,'service_reciprocal':service_reciprocal,'dual_service_allocation':dual_service_allocation,
 'joint_physical':joint_physical,'joint_sales':joint_sales,'joint_nrv':joint_nrv,'single_cash_flow_time_value':single_cash_flow_time_value,
 'eoq':eoq,'reorder_point':reorder_point,'percentage_comparison':percentage_comparison,'weighted_group_ratio':weighted_group_ratio,'food_usage_yield':food_usage_yield}

# Scalars that legitimately allow signs. Other numeric scalar inputs are nonnegative,
# with additional positive/range restrictions implemented in their named functions.
SIGNED={
 'operating_leverage':{'sales_change_fraction'},'inventory_profit_reconciliation':{'variable_income'},
 'roi_residual_income':{'income'},'eva_edition':{'after_tax_operating_income'},
 'dated_annual_npv':{'annual_discount_rate'},'conventional_irr':{'lower_rate','upper_rate'},
 'arr_initial':{'average_annual_income'},'arr_average':{'average_annual_income'},
 'profitability_index':{'pv_future_cash_flows'},'nominal_real_rate':{'real_rate','inflation_rate'},
 'single_cash_flow_time_value':{'principal','future_cash_flow','rate'},
 'percentage_comparison':{'old_ratio','new_ratio'},'food_usage_yield':{'net_transfers_in'}}

def validate_value(value: Any, typ: str, name: str) -> None:
    if typ=='number':require(num(value),'type',name+' must be a finite number, not a boolean/string/null')
    elif typ=='integer':require(isinstance(value,int) and not isinstance(value,bool),'type',name+' must be an integer')
    elif typ in {'number_array','integer_array'}:
        require(isinstance(value,list) and len(value)>0,'dimension',name+' must be a nonempty array')
        for i,v in enumerate(value):validate_value(v,'integer' if typ=='integer_array' else 'number',f'{name}[{i}]')
    elif typ=='number_matrix':
        require(isinstance(value,list) and len(value)>0,'dimension',name+' must be a nonempty matrix')
        for i,row in enumerate(value):validate_value(row,'number_array',f'{name}[{i}]')
        require(all(len(row)==len(value[0]) for row in value),'dimension',name+' must be rectangular')
    elif typ=='date':
        require(isinstance(value,str),'type',name+' must be an ISO date string')
        try:d=date.fromisoformat(value)
        except ValueError as e:raise ModelError('type',name+' must be a valid ISO date') from e
        require(d.isoformat()==value,'type',name+' must use YYYY-MM-DD')
    elif typ=='dated_cash_flow_array':
        require(isinstance(value,list) and len(value)>0,'dimension',name+' must be a nonempty dated cash-flow array')
        for row in value:
            require(isinstance(row,dict) and set(row)=={'date','amount'},'type','Each cash flow must have exactly date and amount')
            validate_value(row['date'],'date',name+'.date');validate_value(row['amount'],'number',name+'.amount')
    else:raise ModelError('type','Unknown declared value type: '+typ)

def run_model(record: dict, inputs: dict) -> dict:
    require(isinstance(inputs,dict),'type','Inputs must be an object');spec=record['content'];impl=spec['implementation_id'];expected={i['name'] for i in spec['input_specifications']}
    missing=expected-set(inputs);extra=set(inputs)-expected
    require(not missing,'missing','Missing required inputs: '+', '.join(sorted(missing)))
    require(not extra,'unexpected','Unexpected inputs: '+', '.join(sorted(extra)))
    for item in spec['input_specifications']:
        k=item['name'];v=inputs[k];validate_value(v,item['value_type'],k)
        if item['value_type'] in {'number','integer'} and k not in SIGNED.get(impl,set()):require(v>=0,'domain',k+' must be nonnegative')
    require(impl in IMPLEMENTATIONS,'not_implemented','No allowlisted implementation')
    try:result=IMPLEMENTATIONS[impl](inputs)
    except (OverflowError,ZeroDivisionError) as e:raise ModelError('numeric_range','Computation exceeds a supported numerical range') from e
    outputs={o['name']:o for o in spec['output_specifications']}
    require(set(result)==set(outputs),'implementation_contract','Output fields disagree with specification')
    for name,value in result.items():
        if value is None:require(outputs[name].get('nullable',False),'implementation_contract','Unexpected null output: '+name)
        else:validate_value(value,outputs[name]['value_type'],name)
    return result

def no_duplicate_keys(pairs):
    result={}
    for key,value in pairs:
        if key in result:raise ValueError('Duplicate JSON key: '+key)
        result[key]=value
    return result

def strict_loads(text: str) -> Any:
    def bad_constant(value):raise ValueError('Nonfinite JSON constant: '+value)
    return json.loads(text,object_pairs_hook=no_duplicate_keys,parse_constant=bad_constant)

def strict_load(path: Path) -> Any:return strict_loads(path.read_text(encoding='utf-8'))
def sha(data: bytes) -> str:return hashlib.sha256(data).hexdigest()

def compare(actual: Any,expected: Any,absolute: float,relative: float,path='output') -> list[str]:
    errors=[]
    if isinstance(expected,dict):
        if not isinstance(actual,dict) or set(actual)!=set(expected):return [path+': dictionary keys differ']
        for key in expected:errors.extend(compare(actual[key],expected[key],absolute,relative,path+'.'+key))
    elif isinstance(expected,list):
        if not isinstance(actual,list) or len(actual)!=len(expected):return [path+': array dimensions differ']
        for i,(a,b) in enumerate(zip(actual,expected)):errors.extend(compare(a,b,absolute,relative,f'{path}[{i}]'))
    elif num(expected):
        if not num(actual) or not math.isclose(actual,expected,abs_tol=absolute,rel_tol=relative):errors.append(f'{path}: actual {actual!r}, expected {expected!r}')
    elif actual!=expected:errors.append(f'{path}: actual {actual!r}, expected {expected!r}')
    return errors

def numerical_tests(lib,tests):
    records={r['id']:r for r in lib['records']};results=[]
    for t in tests['numerical_tests']:
        expected=t['expected'];errors=[];actual=None
        try:
            actual={'outcome':'numeric','outputs':run_model(records[t['model_record_id']],t['inputs'])}
        except ModelError as e:actual={'outcome':'blocked','error_code':e.code}
        except Exception as e:actual={'outcome':'unexpected_error','error':type(e).__name__+': '+str(e)}
        errors=compare(actual,expected,t['tolerances']['absolute'],t['tolerances']['relative'])
        results.append({'test_id':t['id'],'model_record_id':t['model_record_id'],'status':'failed' if errors else 'passed','actual':actual,'failures':errors})
    return results

# Structural validation checks the canonical envelope and each family, the full model
# specification, declared enumerations, uniqueness and references across file boundaries.
def structural_checks(data):
    errors=[];checks=0
    def check(ok,msg):
        nonlocal checks
        checks+=1
        if not ok:errors.append(msg)
    lib=data[FILES[0]];source=data[FILES[1]];tests=data[FILES[2]];context=data[FILES[3]];index=data[FILES[7]]
    records=lib.get('records',[]);claims=lib.get('claim_ledger',[]);locs=source.get('source_locators',[]);ts=tests.get('numerical_tests',[])+tests.get('reasoning_tests',[])
    allids=[]
    for name,items in [('record',records),('claim',claims),('locator',locs),('test',ts)]:
        check(isinstance(items,list),name+' collection must be a list');ids=[x.get('id') for x in items];check(all(isinstance(i,str) and i for i in ids),name+' IDs must be nonempty strings');check(len(ids)==len(set(ids)),name+' IDs are duplicated');allids.extend(ids)
    check(len(allids)==len(set(allids)),'IDs collide across namespaces');rid={r['id'] for r in records};cid={c['id'] for c in claims};lid={l['id'] for l in locs};tid={t['id'] for t in ts}
    check(lib['record_counts']==dict(Counter(r['record_type'] for r in records)),'Record count declarations disagree')
    required=['id','record_type','title','primary_question','content','claim_ids','source_locator_ids','related_record_ids','risk_record_ids','applicability_conditions','limitations','evidence_layer','chapter_numbers']
    byid={r['id']:r for r in records}
    for r in records:
        p=r['id'];check(all(k in r for k in required),p+' missing envelope fields');check(r['record_type'] in FAMILIES,p+' invalid record_type');check(r['evidence_layer'] in LAYERS,p+' invalid evidence layer');check(isinstance(r['content'],dict),p+' content must be object')
        for k in ['title','primary_question']:check(isinstance(r[k],str) and bool(r[k]),p+' invalid '+k)
        for k,space in [('claim_ids',cid),('source_locator_ids',lid),('related_record_ids',rid),('risk_record_ids',rid)]:
            check(isinstance(r[k],list) and all(isinstance(v,str) and v in space for v in r[k]),p+' unresolved/wrongly typed '+k)
        check(all(byid[v]['record_type']=='risk' for v in r['risk_record_ids'] if v in byid),p+' risk link is not a risk record')
        for k in ['applicability_conditions','limitations']:check(isinstance(r[k],list) and all(isinstance(v,str) for v in r[k]),p+' invalid '+k)
        check(isinstance(r['chapter_numbers'],list) and all(isinstance(v,int) and not isinstance(v,bool) and 1<=v<=17 for v in r['chapter_numbers']),p+' invalid chapter numbers')
        if r['record_type']=='model':
            c=r['content'];fields=['model_name','decision_supported','input_specifications','output_specifications','formula_components','source_notation','assumptions','valid_range_and_horizon','sign_convention','rounding_policy','input_handling','reconciliation_checks','edge_cases','test_case_ids','implementation_id','source_locator_ids','application_limitations']
            check(all(k in c for k in fields),p+' incomplete model specification')
            for family in ['input_specifications','output_specifications']:
                specs=c[family];check(isinstance(specs,list) and len(specs)>0,p+' empty '+family);names=[s['name'] for s in specs];check(len(names)==len(set(names)),p+' duplicate symbol names')
                for s in specs:
                    check(all(k in s for k in ['name','value_type','unit','period','measurement_basis','allowed_values','meaning']),p+' incomplete symbol definition');check(s['value_type'] in TYPES,p+' invalid symbol type')
                    for k in ['name','unit','period','measurement_basis','allowed_values','meaning']:check(isinstance(s[k],str) and bool(s[k]),p+' empty symbol '+k)
                    if family=='input_specifications':check(s.get('required') is True,p+' input is not explicitly required')
                    else:check(isinstance(s.get('nullable'),bool),p+' output nullable flag absent')
            check(c['implementation_id'] in IMPLEMENTATIONS,p+' implementation not allowlisted');check(all(t in tid for t in c['test_case_ids']),p+' unresolved test IDs');check(len(c['test_case_ids'])>0,p+' has no implemented test');check(all(v in lid for v in c['source_locator_ids']),p+' unresolved model locators');check(bool(c['assumptions']) and bool(c['valid_range_and_horizon']) and bool(c['reconciliation_checks']),p+' lacks applicability controls')
            check(all(isinstance(f,dict) and isinstance(f.get('readable_formula'),str) and bool(f['readable_formula']) for f in c['formula_components']),p+' invalid readable formulas')
        elif r['record_type']=='concept':check(all(k in r['content'] for k in ['explanation','distinctions','diagnostic_questions']),p+' incomplete concept payload')
        elif r['record_type']=='risk':check(all(k in r['content'] for k in ['failure_mode','diagnostic_check','required_response']),p+' incomplete risk payload')
        elif r['record_type']=='application':check(all(k in r['content'] for k in ['required_project_evidence','procedure','data_status']),p+' incomplete application payload');check(r['evidence_layer']=='application_extension',p+' mislabeled application')
        elif r['record_type']=='route':check(all(x in rid for x in r['content']['retrieval_record_ids']),p+' unresolved route target');check(isinstance(r['content']['required_evidence'],list),p+' route evidence must be a list')
        elif r['record_type']=='decision':
            check(all(k in r['content'] for k in ['baseline','alternative','incremental_revenues','incremental_costs','avoidable_versus_continuing','capacity_and_opportunity_cost','time_horizon','demand_and_pricing_assumptions','qualitative_contractual_operational_consequences','what_changes_the_recommendation','model_record_ids']),p+' incomplete decision payload')
            for k in ['incremental_revenues','incremental_costs','qualitative_contractual_operational_consequences','what_changes_the_recommendation']:check(isinstance(r['content'][k],list) and all(isinstance(v,str) for v in r['content'][k]),p+' invalid decision '+k)
            check(all(v in rid and byid[v]['record_type']=='model' for v in r['content']['model_record_ids']),p+' invalid decision-model link')
        elif r['record_type']=='workflow':check(r['evidence_layer']=='application_extension' and bool(r['content']),p+' workflow must be a nonempty application extension')
    for c in claims:
        check(c['basis'] in BASES,c['id']+' invalid claim basis');check(isinstance(c['proposition'],str) and bool(c['proposition']),c['id']+' empty proposition');check(all(v in lid for v in c['supporting_source_locator_ids']),c['id']+' unresolved locator')
        for k in ['source_fidelity_status','numerical_verification_status','current_verification_status','project_applicability']:check(c[k] in STATUSES,c['id']+' invalid '+k)
        check(isinstance(c['conditions_and_qualifications'],list) and all(isinstance(v,str) for v in c['conditions_and_qualifications']) and isinstance(c['unresolved_questions'],list) and all(isinstance(v,str) for v in c['unresolved_questions']),c['id']+' invalid qualifications/questions')
        check(c['source_fidelity_confidence']['rating'] in {'high','medium','low','not_applicable'},c['id']+' invalid confidence rating')
        check(all(t in tid for t in c.get('numerical_verification_test_ids',[])),c['id']+' unresolved numerical test links')
    for l in locs:
        check(l['source_file_id'] in {f['id'] for f in source['source_files']},l['id']+' unknown source file')
        check(l['checked_against_source'] in STATUSES,l['id']+' invalid source-check status')
        check(isinstance(l['internal_filename'],str) and l['internal_filename'].startswith('OEBPS/'),l['id']+' invalid internal path')
        check(l['anchor_id'] is None or isinstance(l['anchor_id'],str),l['id']+' invalid anchor type')
    for c in source['chapter_coverage']+source['supplementary_appendix_coverage']:
        check(c['coverage_status'] in STATUSES,'Invalid chapter/appendix coverage status')
        check(all(v in rid for v in c['record_ids']),'Coverage contains unresolved record IDs')
        check(all(v in lid for v in c['source_locator_ids']),'Coverage contains unresolved source locators')
    for t in tests['reasoning_tests']:
        check(t['data_origin']=='original_synthetic',t['id']+' reasoning data origin is not synthetic')
    check(tests['counts']=={'numerical_tests':len(tests['numerical_tests']),'reasoning_tests':len(tests['reasoning_tests']),'models_exercised':len({t['model_record_id'] for t in tests['numerical_tests']})},'Test suite counts disagree')
    for t in tests['numerical_tests']:
        check(t['model_record_id'] in rid,t['id']+' unresolved model');check(t['implementation_id'] in IMPLEMENTATIONS,t['id']+' unknown implementation');check(t['expected']['outcome'] in {'numeric','blocked'},t['id']+' invalid expected outcome');check(isinstance(t['independent_derivation'],str) and bool(t['independent_derivation']),t['id']+' missing independent derivation')
        if t['model_record_id'] in byid:check(t['implementation_id']==byid[t['model_record_id']]['content']['implementation_id'],t['id']+' model/implementation mismatch')
    for t in tests['reasoning_tests']:
        check(t['review_status'] in STATUSES,t['id']+' invalid reasoning review status');check(all(v in rid for v in t['record_ids']),t['id']+' unresolved reasoning reference')
    # Review references in auxiliary nested payloads without treating filenames as IDs.
    def walk_refs(o,path=''):
        if isinstance(o,dict):
            for k,v in o.items():
                if k.endswith('_record_id') and isinstance(v,str):check(v in rid,path+'.'+k+' unresolved')
                if k.endswith('_record_ids') and isinstance(v,list):check(all(i in rid for i in v),path+'.'+k+' unresolved')
                walk_refs(v,path+'.'+k)
        elif isinstance(o,list):
            for v in o:walk_refs(v,path)
    for obj in [records,context]:walk_refs(obj)
    check(set(f['filename'] for f in index['files'])==set(FILES),'File index does not describe exactly the nine deliverables')
    for f in index['files']:check(all(d in FILES for d in f['dependencies']),f['filename']+' unknown dependency')
    return {'status':'failed' if errors else 'passed','checks_run':checks,'failures':errors,'scope':'Envelope and family contracts, symbol types, enumerations, duplicate IDs, references, counts and file dependencies. Human meaning and applicability are separate.'}

def source_blocks(xmlbytes: bytes):
    root=ET.fromstring(xmlbytes);blocks=[]
    def walk(el,nested=False):
        tag=el.tag.split('}')[-1]
        if tag in {'h1','h2','h3','h4','h5','h6','p','table'} and not nested:
            txt=' '.join(s.strip() for s in el.itertext() if s.strip())
            if txt or any(child.tag.split('}')[-1]=='img' for child in el.iter()):blocks.append(txt)
        for child in el:walk(child,nested or tag in {'p','table'})
    walk(root)
    return root,blocks

def source_checks(source: dict, source_zip: Path|None):
    if source_zip is None or not source_zip.is_file():return {'status':'blocked','locator_integrity_status':'blocked','reason':'Original uploaded ZIP was not supplied to this run; source bytes cannot be rechecked.','checked_locators':0,'failures':[],'interpretation_audit':'requires_human_review'}
    errors=[];count=0;imagecount=0;source_hash_ok=False
    try:
        require(sha(source_zip.read_bytes())==source['source_files'][0]['sha256'],'source_hash','Original source ZIP hash does not match recorded upload')
        source_hash_ok=True
        with zipfile.ZipFile(source_zip) as z:
            prefix=source['source_files'][0]['zip_book_root'];names=set(z.namelist());cache={}
            for loc in source['source_locators']:
                path=prefix+loc['internal_filename']
                if path not in names:errors.append(loc['id']+': internal file missing');continue
                if path not in cache:cache[path]=source_blocks(z.read(path))
                root,blocks=cache[path];anchor=loc.get('anchor_id')
                if anchor and not any(e.attrib.get('id')==anchor for e in root.iter()):errors.append(loc['id']+': anchor missing');continue
                if 'block_selection' in loc:
                    a=loc['block_selection']['start_zero_based'];b=loc['block_selection']['end_zero_based_inclusive']
                    if not (0<=a<=b<len(blocks)):errors.append(loc['id']+': block range invalid');continue
                    digest=sha('\n'.join(blocks[a:b+1]).encode())
                    if digest!=loc['normalized_selection_sha256']:errors.append(loc['id']+': normalized source span hash differs');continue
                elif 'raw_file_sha256' in loc and sha(z.read(path))!=loc['raw_file_sha256']:errors.append(loc['id']+': metadata file hash differs');continue
                count+=1
            for image in source.get('visual_reviews',[]):
                path=prefix+image['internal_filename']
                if path not in names or sha(z.read(path))!=image['sha256']:errors.append('Reviewed image missing or changed: '+path)
                else:imagecount+=1
    except Exception as e:errors.append(type(e).__name__+': '+str(e))
    return {'status':'failed' if errors else 'requires_human_review','locator_integrity_status':'failed' if errors else 'passed','source_hash_checked':source_hash_ok,'checked_locators':count,'reviewed_image_assets_rechecked':imagecount,'failures':errors,'interpretation_audit':'requires_human_review','scope':'Actual uploaded ZIP, real internal paths/anchors, selected normalized text-span hashes and reviewed image hashes. This is not an independent expert audit of every paraphrase or exhaustive chapter coverage.'}

def self_tests():
    results=[]
    for name,bad in [('duplicate_key','{"a":1,"a":2}'),('nan_constant','{"a":NaN}'),('infinity_constant','{"a":Infinity}')]:
        try:strict_loads(bad);ok=False
        except ValueError:ok=True
        results.append({'test':name,'status':'passed' if ok else 'failed'})
    return results

def checksum_checks(directory: Path,manifest: dict,enabled: bool):
    if not enabled:return {'status':'not_run','reason':'Invoke with --check-checksums after final payload and report are frozen.'}
    errors=[];expected=set(FILES)-{FILES[-1]};items=manifest.get('files',{})
    if set(items)!=expected:errors.append('Checksum manifest must cover exactly the other eight deliverables')
    for name,digest in items.items():
        path=directory/name
        if name not in expected:continue
        if not path.is_file() or sha(path.read_bytes())!=digest:errors.append('Hash mismatch or missing: '+name)
    return {'status':'failed' if errors else 'passed','files_checked':len(items),'failures':errors,'checksum_file_self_hash':'excluded by design'}

def validate(directory: Path,source_zip: Path|None=None,check_checksums=False):
    loaded={};parse_errors=[]
    for name in FILES:
        path=directory/name
        if not path.is_file():parse_errors.append('Missing file: '+name);continue
        if name.endswith('.json'):
            try:loaded[name]=strict_load(path)
            except (ValueError,OSError) as e:parse_errors.append(name+': '+str(e))
    report={'report_version':'1.0.0','executed_at_utc':datetime.now(timezone.utc).isoformat(),'execution_environment':{'python':sys.version.split()[0],'network_used':False,'software_scope':'Local Python synthetic functions only; no company workbook, SQL or BI execution.'},'strict_json':{'status':'failed' if parse_errors else 'passed','json_files_parsed':len(loaded),'failures':parse_errors},'validator_self_tests':self_tests()}
    if parse_errors:report['overall_status']='failed';return report
    try:struct=structural_checks(loaded)
    except Exception as e:struct={'status':'failed','failures':['Structural validator could not proceed: '+type(e).__name__+': '+str(e)]}
    report['structural']=struct;lib=loaded[FILES[0]];source=loaded[FILES[1]];tests=loaded[FILES[2]]
    report['source']=source_checks(source,source_zip)
    nr=numerical_tests(lib,tests);counts=Counter(r['status'] for r in nr);tested={r['model_record_id'] for r in nr};models=[r for r in lib['records'] if r['record_type']=='model']
    report['numerical']={'status':'failed' if counts['failed'] else 'passed','tests_run':len(nr),'passed':counts['passed'],'failed':counts['failed'],'implemented_models_exercised':len(tested),'models_not_exercised':[r['id'] for r in models if r['id'] not in tested],'expected_results_method':'Literal independently derived synthetic expectations stored separately from implementation; no textbook exercises or solutions.','results':nr}
    # Machine checks preserve formal distinctions; they cannot certify causal meaning.
    invariants=[{'name':'application_records_labeled','passed':all(r['evidence_layer']=='application_extension' for r in lib['records'] if r['record_type']=='application')},{'name':'purchase_and_usage_models_separate','passed':{'ma-model-material-purchase-price','ma-model-material-usage-variances'}<= {r['id'] for r in models}},{'name':'distinct_arr_denominators','passed':{'ma-model-arr-initial','ma-model-arr-average'}<={r['id'] for r in models}},{'name':'no_external_claims_falsely_verified','passed':not any(c['basis']=='verified_external_material' for c in lib['claim_ledger'])},{'name':'no_real_company_test_results','passed':all(t.get('data_origin')=='original_synthetic' for t in tests['numerical_tests'])}]
    report['semantic']={'status':'requires_human_review' if all(x['passed'] for x in invariants) else 'failed','machine_invariants':invariants,'manual_reasoning_cases':len(tests['reasoning_tests']),'reasoning_case_status':'requires_human_review','boilerplate_review':source['editorial_review']['boilerplate_review'],'limit':'No programmatic test establishes source interpretation, causality, or the quality of a business recommendation.'}
    report['applicability']={'status':'requires_human_review','model_specification_completeness':'passed' if struct['status']=='passed' else 'failed','project_data_supplied':False,'scope':'Assumptions, units, periods, signs, boundaries and reconciliations are specified. A qualified project reviewer must confirm suitability and company policy before real use.'}
    report['currentness']={'status':'blocked','independently_verified_external_claims':0,'reason':'Web access was disabled. Source-era tax, legal, company and accounting examples are not current authority; software documentation was not independently checked.','current_claim_policy':'No current legal, tax, market, company or software claim is asserted as independently verified.'}
    report['checksums']=checksum_checks(directory,loaded[FILES[-1]],check_checksums)
    report['counts']={'records':len(lib['records']),'record_families':lib['record_counts'],'claims':len(lib['claim_ledger']),'source_locators':len(source['source_locators']),'chapters_with_selected_substantive_reading':len(source['chapter_coverage']),'supplementary_appendices_with_selected_reading':len(source['supplementary_appendix_coverage'])}
    failed=any(report[k]['status']=='failed' for k in ['strict_json','structural','source','numerical','semantic','checksums']) or any(t['status']=='failed' for t in report['validator_self_tests'])
    report['overall_status']='failed' if failed else 'requires_human_review';report['interpretation']='Passed numerical and structural checks are not professional assurance, complete source coverage or approval of a company decision.'
    return report

def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--package-dir',type=Path,default=Path(__file__).resolve().parent);p.add_argument('--source-zip',type=Path);p.add_argument('--report',type=Path,help='Write a new report explicitly; packaged hashes then need regeneration if this replaces the packaged report.');p.add_argument('--check-checksums',action='store_true');args=p.parse_args()
    report=validate(args.package_dir,args.source_zip,args.check_checksums);text=json.dumps(report,ensure_ascii=False,indent=2,allow_nan=False)+'\n'
    if args.report:args.report.write_text(text,encoding='utf-8')
    else:print(text,end='')
    return 1 if report['overall_status']=='failed' else 0
if __name__=='__main__':raise SystemExit(main())
