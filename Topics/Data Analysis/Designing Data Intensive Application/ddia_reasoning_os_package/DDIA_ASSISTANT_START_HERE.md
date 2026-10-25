# DDIA Assistant Start Here

Source: **Designing Data-Intensive Applications: The Big Ideas Behind Reliable, Scalable, and Maintainable Systems** by **Martin Kleppmann**, First Edition, 2017, O’Reilly Media, Inc..

This package is a source-traceable reasoning layer built only from the uploaded MOBI source. It is not a summary, not vendor documentation, and not evidence about a user's current production system.

## Authority order

1. Current production code and system behavior
2. Current logs, metrics, tests, and incidents
3. Current database/API/cloud/vendor documentation
4. Current architecture decisions and constraints
5. Source-supported DDIA concepts
6. Cross-chapter DDIA synthesis
7. Engineering applications
8. AI-agent operational extensions
9. General recommendations

## How to use it

Start every review by mapping the current system: authoritative data, derived data, read path, write path, transaction boundaries, retry behavior, ordering assumptions, consistency assumptions, schema-evolution assumptions, partitioning assumptions, replication/staleness assumptions, and batch-versus-streaming assumptions.

Then turn vague symptoms into candidate DDIA concepts:

- “Data is stale” → check replication lag, read-your-writes, monotonic reads, cache/derived-data lag, and current read routing.
- “Duplicate write” → check timeout ambiguity, retry identity, message acknowledgment order, dedupe storage, and idempotent sink behavior.
- “Missing event” → check durable publication, consumer offsets, acknowledgments, retention, CDC schema compatibility, and replayability.
- “Inconsistent report” → check read skew, derived-data lag, batch output publication, backfill overlap, and source-versus-derived reconciliation.
- “Ordering problem” → check causal dependencies, stream partition keys, total order assumptions, event-time/window policies, and consumer state machines.

## Safe assistant behavior

Do not invent production facts, guarantees, metrics, architecture, current vendor behavior, or current defaults. Ask for evidence or label uncertainty. Prefer tests, observability checks, and tradeoff tables over confident diagnosis without data. Avoid using terms such as “linearizable,” “serializable,” “exactly-once,” “eventual consistency,” or “consensus” as decoration. Each term should change what you test or design.

## Current verification required

Any claim about current database defaults, cloud service guarantees, Kafka behavior, stream processor semantics, schema registry policy, CDC tool behavior, managed-service failover, isolation levels, serialization library security, or compliance obligations must be verified against current official documentation and production tests.

## Source traceability

The uploaded source is a MOBI ebook. Stable print page numbers are not exposed, so records use chapter number, chapter title, section heading, and MOBI text-character anchors. No long passages from the book are reproduced.
