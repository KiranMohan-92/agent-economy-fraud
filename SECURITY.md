# Security notice

Historical revisions contained a live-looking Dune API credential in source.
The current tree removes all embedded fallback credentials and reads
`DUNE_API_KEY` only from the environment.

Repository cleanup does not revoke a credential. The credential owner must:

1. revoke and rotate the exposed key at the provider;
2. inspect provider access logs and quotas for unauthorized use;
3. scan Git history, forks, build logs, archives, and releases;
4. enable repository secret scanning and push protection; and
5. keep future secrets in an approved secret store or local environment only.

Do not paste the historical value into an issue, report, or rotation record.
