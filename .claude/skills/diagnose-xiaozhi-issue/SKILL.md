---
name: diagnose-xiaozhi-issue
description: Diagnose and resolve xiaozhi-esp32-server issues systematically by identifying symptoms, tracing root causes, and providing step-by-step fixes. Use when encountering container failures, OTA connectivity problems, configuration errors, or deployment issues in xiaozhi-esp32-server.
---

# Diagnose Xiaozhi-ESP32-Server Issues

A systematic troubleshooting skill for xiaozhi-esp32-server deployments. Covers authentication, OTA connectivity, configuration drift, container networking, and upgrade failures.

## Workflow

### 1. Capture the Symptom

Ask the user ONE question: **"What's the exact error or behavior you're seeing?"**

Do NOT ask follow-ups yet. Move directly to step 2.

### 2. Diagnose the Root Cause

Based on the symptom, trace to one of these problem categories:

| Symptom | Category | Ref |
|---------|----------|-----|
| Container repeatedly restarting, API returns 401 | Server Secret Mismatch | [REFERENCE.md](#server-secret-mismatch) |
| Device can't connect to OTA, returns 404 | OTA Connection Error | [REFERENCE.md](#ota-connection-error) |
| OTA upgrade fails, device auto-update stuck | OTA Upgrade Failure | [REFERENCE.md](#ota-upgrade-failure) |
| Server IP changed, devices disconnect | IP Change Issue | [REFERENCE.md](#ip-change) |
| Container port confusion, can't reach service | Port Mapping | [REFERENCE.md](#container-ports) |

Run the quick diagnostic commands for that category:

```bash
# Universal checks
docker ps -a | grep xiaozhi                    # Check container status
docker logs xiaozhi-esp32-server --tail 100    # Check latest errors
docker inspect xiaozhi-esp32-server            # Check config/env
```

### 3. Apply Fix

Once you identify the category:

- **List the exact commands** the user needs to run (in order)
- **Explain WHY** each command fixes the root cause
- **Provide verification steps** to confirm the fix worked

Never just say "clear Redis" — explain the symptom chain (e.g., "Redis cached an old secret, so even though the database updated it, the server still validates against the old value").

### 4. Verify & Document

After the user runs the fix:

- [ ] Confirm the symptom is gone
- [ ] Suggest preventive steps (e.g., update your notes, pin the IP in config, etc.)
- [ ] Ask if they'd like to add a custom alert rule to catch this sooner

## Diagnosis Checklist

When troubleshooting, follow this order:

1. **Container health** - Is it running? Restarting? Healthy?
2. **Logs** - What's the actual error message?
3. **Configuration alignment** - Config file vs database vs runtime state
4. **Network connectivity** - Can containers reach each other? Can clients reach containers?
5. **Cache consistency** - Are Redis/in-memory caches stale?

## Common Fix Patterns

| Pattern | Command |
|---------|---------|
| Clear stale cache | `docker exec xiaozhi-esp32-server-redis redis-cli del <key>` |
| Force reload config | `docker restart xiaozhi-esp32-server` |
| Check database state | `docker exec xiaozhi-esp32-server-db mysql -u<user> -p<pass> -e "<query>"` |
| View container env | `docker inspect xiaozhi-esp32-server --format='{{json .Config.Env}}'` |
| Test internal connectivity | `docker run --rm --network xiaozhi-server_default alpine wget -qO- http://<service>:<port>/<path>` |

---

**For detailed troubleshooting guides, see [REFERENCE.md](REFERENCE.md)**
