# SOP: Studio Engine - Git Lineage Recovery (Main Authority Protocol)

**Role:** Autonomous Repository Maintainer
**Domain:** Codebase Health (@fivepanelhat repositories)

## Execution Protocol: Pre-Merge Verification
1. **Verify Lineage:** Before generating a Pull Request, execute `skill-verify-lineage` comparing your working branch to `main`.
2. **Evaluate Output:**
   - If `status == "ahead"` or `"diverged"` with a valid `common_ancestor_sha`: Proceed with standard PR creation.
   - If `status == "orphaned"`: **HALT**. Your branch history is detached. `main` holds absolute authority.
3. **Recovery Tactic (The "Authoritative Graft"):**
   - You must abandon your orphaned commit history but salvage your file artifacts.
   - Execute exactly:
     `git fetch origin main`
     `git reset --hard origin/main`
     `git restore --source origin/<your-branch-name> .`
     `git add .`
     `git commit -m "chore: autonomous graft of agent artifacts onto main"`
     `git push --force origin <your-branch-name>`
   - Proceed to open the Pull Request.
