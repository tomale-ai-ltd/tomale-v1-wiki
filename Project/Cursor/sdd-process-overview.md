---
type: foundation
title: sdd-process-overview
status: current
project: tomale-rn-v1
date: 2026-04-14
---
___

# Process Overview

> Relates to the sdd (spec driven development) process and how this is being used alongside the specification, using core technologies, to develop the tomale-rn-v1 app.


## **Setup Tasks \(once per project\)**

1. Create \.docs&#x2F;prd at root level\.
2. Place example\.md file inside \.docs&#x2F;prd \- **this is the micro\-prd template to be used for each future slice &#x2F; sub\-slice\.**

## **For each slice \(repeat\)**

1. Create a folder for each slice in \.docs&#x2F;prd&#x2F;**\[000\-slicename\-subslice\]**
2. Numbering follows 000,002,003 onwards as per speckit feature naming conventions\.

## **For Each Sub\-slice \(repeat\)**

1. Inside the specs folder, create a \.md micro\-prd for each sub\-slice, **e\.g\. 001\-slicename\-subslice\.md**
2. Directory should read **\.docs&#x2F;prd&#x2F;001\-slicename\-subslice\.md, \.docs&#x2F;prd&#x2F;002\-slicename\-subslice\.md** etc**\.**

## **For Each Sub\-slice \(repeat\)**

1. Create new branch with **001\-slicename\-subslice naming convention**
2. Use **&#x2F;speckit\.specify** cursor command to create the directory structure for future AI generated documents\. Be sure to reference **\.docs&#x2F;prd&#x2F;001\-slicename\-subslice\.md in prompt\.**
3. Review the documents created by speckit\.specify to **ensure parity with micro\-prd and constitution**\.
4. Use **speckit\.plan** to **create the implementation plan\.**
5. Use **speckit\.clarify** to **interrogate and improve the plan**\. At this point refer to &#39;**foundation\-impact\-assessment\.md**&#39; in docs and ask clarify to consider this\.
6. Use **speckit\.tasks** to **create the dev tasks**\.
7. Use **speckit\.analyze** to perform a **read\-only analysis** of the spec, plan and tasks created for the feature\. Make changes using specify, plan and&#x2F;or tasks as desired\.
8. Use **speckit\.implement** to **implement the feature and run tests** before committing\.
9. Instruct speckit\.implement to create a **validation\.md** file inside **specs&#x2F;001\-slicename\-subslice&#x2F;checklists** folder\. Run through these items with the agent to validate the implementation has been carried out properly\.
10. **Commit all** changes to current feature branch\.
11. Process **GitHub PR**, **squash and merge**, then **delete** branch\.

