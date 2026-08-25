# Server Identification

## Context and Problem Statement

SchemaCrawler needs a stable, privacy-aware way to identify a database server
for downstream consumers such as Scribe generated OKF and the SchemaCrawler AI MCP server.

## Considered Options

1. **Find host location**

   Probe the live database for a human-readable location or instance
   name.

   This is the most descriptive option, but it remains connector-specific,
   depends on SQL access, and does not scale well as a core identity model.

2. **Use raw JDBC host information**

   Use the hostname, IP address, or full JDBC URL as the identity.

   This is simple, but it exposes sensitive location details and is unstable
   across URL formatting differences, aliases, and deployment environments.

3. **Use a salted or per-installation hash**

   Hash the raw server info data with a local salt.

   This improves privacy, but it prevents correlation across systems and makes
   the identifier less useful for OKF and AI MCP server scenarios where the same
   server needs to be recognized consistently.

4. **Use a deterministic fingerprint from normalized JDBC inputs**

   Parse the JDBC URL, classify and normalize the host, hash public hostnames
   before storage, and compute a SHA-256 fingerprint from the normalized server
   type, host hash, database name, and database product version.

   This is the chosen direction.

## Decision Outcome

SchemaCrawler needs a deterministic, privacy-aware server fingerprint.

The proposed implementation uses an identifier based on normalized JDBC data
rather than raw server probes:

- `JdbcUrlParser` owns host classification and host hashing
- `JdbcUrl` stores normalized values, not raw host text
- `DatabaseServerFingerprintBuilder` hashes the canonical server inputs into a
  single fingerprint and attaches confidence metadata

This is the best fit for OKF and the AI MCP server because it is:

- **stable** across repeated runs
- **safe** to store and compare
- **deterministic** without requiring extra SQL probes
- **practical** when only partial JDBC metadata is available

The trade-off is that the fingerprint is intentionally not a proof of a unique
physical machine. The current algorithm omits the port and uses the JDBC server
type as the product-family discriminator, so it behaves like a coarse server
identity rather than a strict instance identifier.

That trade-off is acceptable because the feature is meant for correlation and
comparison, not authentication. Confidence scoring makes the uncertainty
visible:

- **High confidence** when host, database name, and version line up
- **Medium confidence** when the URL is partly normalized or partially
  specified
- **Low confidence** when the input is sparse or ambiguous

## Consequences

- Sensitive host/IP data is normalized before it reaches the fingerprint.
- The identifier is portable and repeatable, which makes it useful for OKF and
  the AI MCP server.
- The fingerprint should be treated as a best-effort identity, not a guarantee
  that two connections hit the same physical server.
