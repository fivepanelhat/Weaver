# SOP: Studio Engine - Git Lineage Recovery

**Role:** Autonomous Repository Maintainer
**Domain:** Codebase Health (@fivepanelhat repositories)

## Execution Protocol: Pre-Merge Verification
1. **Verify Lineage:** Before generating a Pull Request, you must execute `skill-verify-lineage` comparing your working branch to `main`.
2. **Evaluate Output:**
   - If `status == "ahead"` or `"diverged"` with a valid `common_ancestor_sha`: Proceed with standard PR creation.
   - If `status == "orphaned"`: **HALT**. The branch histories are unrelated. GitHub cannot compare them.
3. **Recovery Tactic (The "Orphan" Fix):**
   - If your working branch contains critical artifacts, you must surgically graft them onto the main timeline.
   - Execute locally: `git fetch origin main`
   - Execute locally: `git merge origin/main --allow-unrelated-histories -m "chore: force merge unrelated agent histories"`
   - Resolve any immediate conflicts favoring your generated artifacts, then push the grafted branch to `origin`.
