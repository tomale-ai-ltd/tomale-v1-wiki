---
type: source
origin: user-note
date: 2026-10-22
tags:
  - llm-wiki/source
aliases: []
cssclasses: []
---


# Project/Decisions/restrict-store-orders-message-to-buyer-gift-message.md

This document outlines a decision regarding the handling of gift messages in store orders, specifying that the buyer's gift message will be stored separately from callback text from HPBC/Pureprint.

## Entities

- [[tomale-rn-v1|Tomale-rn-v1]]
- [[hpbc-aka-pureprint|HPBC (aka Pureprint)]]

## Concepts

- [[hpbcupdateorder|hpbc_update_order]]
- [[storeordersmessage|store_orders.message]]
