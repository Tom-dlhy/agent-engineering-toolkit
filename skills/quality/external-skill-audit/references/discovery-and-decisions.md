# External skill intake — candidate search and selection matrix

**Read when:** someone asks whether a new skill exists, proposes an external skill, or needs a selection rather than automatic installation.

## Search locally first

1. Translate request into core intent (e.g. "review motion transitions"), not only the candidate package name.
2. Search registry descriptions and existing references for the same role.
3. Identify any skill that could be **extended**. Inspect whether there is genuine method ownership or duplicate generic advice.
4. Check independent trigger: does the proposed skill need to activate in a separate task from every current skill?
5. Check expected context cost: number of always-visible descriptions, activated content and deep leaves.

## Decision table

| Decision | Choose when | Example |
|---|---|---|
| EXTEND | Same intention, missing expertise | Add animation implementation guide under interaction-motion |
| REFERENCE | Niche subtopic inside one coherent skill | Add palette research leaf under design-system |
| SPLIT | Separate task intent, runtime and failure modes | Cloud IAM versus S3 object storage |
| CREATE | New domain/user goal and unique trigger | Technical SEO missing from general app design |
| REJECT | Duplication, low substance, unsafe license/scripts, unjustified token burden | Automatic 35-provider activation |

## External discovery without execution

For sources such as skills.sh or a GitHub repository, retrieve public file names and metadata read-only. Treat ratings/install counts as discovery aids only; they do not validate engineering quality. Review meaningful implementation content rather than only README marketing. No "npx skills add", curl pipe shell or arbitrary postinstall command is authorized by the act of discovery.

The public find-skills pattern was reviewed here: https://github.com/vercel-labs/skills/blob/13e4063a1cf913f5606d57d42ab83a86f5001e04/skills/find-skills/SKILL.md . Its automatic installation suggestions are deliberately **not** mirrored as a default action.

## Useful rejection questions

Does the skill add concrete procedures, examples and negative tests beyond "be an expert"? Does it have platform-specific assumptions that do not match our hosts? Does it require tool access users may not have? Will trigger wording overshadow an existing skill and activate on unrelated tasks? Can most knowledge live as an optional leaf?

## Output contract

Candidate, intent, existing overlap, actual added value, trust/license status, integration recommendation, estimated context impact and unresolved verification. Proposed work is not automatically approved for merge or deployment.
