# Transcript: Engineering Sync – Code Refactor and Observability Improvements

**Date:** 2025-05-30

## Discussions

**[00:00:02] Loretta Perez:**  
Alright, folks, thanks for making the time today. I know everyone's knee-deep in various threads, but this session should help align a few of them — namely the ongoing module refactor and some of the observability pain points we flagged last week. The goal is to come out of this with fewer unknowns and ideally fewer late-night Slack pings. Let's start with the refactor. Rachel, you’ve been leading most of the `EventRouter` changes — can you give us a rundown of where things stand?

**[00:00:29] Rachel Aguirre:**  
Yep, absolutely. So, we’ve made solid progress on decoupling the event logic from the main `GameCore`. Right now, the `EventRouter` handles the majority of broadcasts, which makes it way easier to track who’s listening to what and also isolates the dependencies a bit better. That said, there’s still a handful of components that are holding onto direct references to `GameCore`, and they’re not easy to untangle because they rely on some of the old synchronous state.

I’m thinking we flag them as deprecated for now and wrap them in an adapter layer — just to avoid breaking anything mid-cycle — and then slowly phase them out as we introduce more atomic components. One thing I’d love to get opinions on is whether we enforce the new routing standard through linter rules or just code review agreements for now.

**[00:01:10] Michael Rogers:**  
Yeah, so I ran into this yesterday. While I was working on the enemy spawner logic, I noticed it’s still tightly coupled to the old init method in `GameCore`. I wasn’t sure if I should rewrite the entire thing or just patch it temporarily. It’s not even using the new event system — it’s literally reaching in to fetch references directly.

I hesitated to make the change because I wasn’t sure if I’d be stepping on someone’s toes, or introducing instability, especially with the upcoming QA sprint. But I agree — we either treat this as technical debt we’re okay with or draw a hard line and say “this gets rewritten or it doesn’t ship.”

**[00:01:45] Loretta Perez:**  
I’m glad you brought that up. Honestly, I’m leaning toward the second option — draw the line. I’d rather break something now, while we have context and time to fix it, than six months from now when nobody remembers how the logic was wired together. Just make it clear in your PR what’s being changed and why, and if you’re ripping out legacy bindings, please leave a trail of notes for QA to reference.

We’ve done the soft-deprecation thing too many times. This time we clean house. If something still talks to `GameCore`, treat it as a red flag and escalate it. Michael, I say go ahead and modernize the enemy spawner fully — if it breaks, we fix it fast.

**[00:02:30] Roger Perez:**  
Alright, quick pivot to the observability topic — I wanted to flag something I found over the weekend. During the deployment window, I was tailing logs out of habit — you know, just one of those late-night rituals — and I caught a bunch of null reference exceptions related to our health check system.

They weren’t fatal, but none of them got reported to Sentry. Turned out the issue was with how the `heartbeat_type` was being passed. Someone changed the key from `"HEARTBEAT_TYPE"` to lowercase `"heartbeat_type"`, and because our schema validator doesn’t exist yet, nothing caught it. So the errors were just… happening silently. It’s kind of scary, honestly.

**[00:03:05] Rachel Aguirre:**  
Oh no… I think that might’ve been me. I remember looking at an older doc that listed the keys in lowercase and thought I was just matching convention. That was in the quick patch I did for the internal instance reporting. I didn’t think it would cascade like that.

**[00:03:21] Roger Perez:**  
Totally understandable — I’m not here to point fingers. Honestly, that just shows we need something in place to catch that sort of thing automatically. If we had even a basic JSON schema validation pass, it would’ve thrown an error before shipping.

**[00:03:34] Loretta Perez:**  
Agreed. And it doesn’t need to be fancy. Roger, if you’ve got something prototyped, let’s get it in. I don’t want us to wait for a bigger observability rework to start putting out these smaller fires. Can we treat this as an immediate follow-up?

**[00:03:47] Roger Perez:**  
Absolutely. I already started wiring in `fastjsonschema` last night. It’s super lightweight and integrates cleanly with our existing logger wrapper. I’ll open a PR today and flag it as high priority. No big dependencies — just a couple of defensive checks before dispatch.

**[00:04:10] Michael Rogers:**  
On a related note, I was looking at the disconnect logs last week — trying to build some simple dropout metrics for QA — and I realized we’re logging disconnects in two totally different formats. One from the server side, one from the auth bridge. The timestamps don’t match, and the structure’s all over the place. It made it really hard to stitch together a clean story of what actually happened when a player dropped.

**[00:04:31] Rachel Aguirre:**  
That’s definitely my bad. I was focused on getting logging in fast during the last rollback sprint. But yeah, that’s messy and needs to be cleaned up. I can take that on. I’ll standardize everything under something like `player.connection.status` and make sure we use a single formatter across all pipelines.

Also — just to be safe — I’ll wrap the new format in a feature flag so we don’t break any dashboards that might be consuming the current version.

**[00:05:05] Loretta Perez:**  
Perfect. That was a solid discussion. I honestly feel like we’re operating with a good rhythm now — tackling tech debt while still shipping visible value. And I just want to say — I really appreciate how each of you balances pragmatism with long-term thinking.

Michael, the way you’ve been approaching test coverage even when the codebase is messy — it doesn’t go unnoticed. Rachel, you’ve taken ownership of some pretty gnarly pieces lately, and you’ve been shipping steadily without drama. Roger, your logs are half the reason we sleep at night.

Let’s keep the momentum. We’ll sync again next week, but feel free to over-communicate in the channel if you’re blocked. Don’t let “waiting for the next standup” be the reason something stalls.

**[00:05:45] END OF TRANSCRIPT**
