# Flexciton Take Home Challenge

## Challenge Description (as given)
### The Problem

Our friend Gary is a very active person with lots of hobbies and social activities, and he never says no to anything. Unfortunately, Gary is also really bad at keeping a schedule. As a result, he often ends up committing to multiple events at the same time.

During a lunch appointment which Gary managed to attend, he told us about this problem. Since Gary knows we specialise in scheduling, he
asked for our help. These were his requirements:

- I do not want to cancel any commitment.
- I only want to do things on weekdays Monday - Friday between 09:00 and 18:00.
- If I've agreed to do things outside those hours, I want those events re-scheduled to the next possible time.
- If I've agreed to do more than one thing at the same time, I want to keep one of the commitments and re-schedule the rest to the next possible time.

### The Task

To help Gary with his scheduling issues, you have been tasked by your Tech Lead with building a command line tool that will take a list of events as an input (one per line) and output a time-ordered list of events.

The output should consist of a list of events, ordered by start date where all Gary’s requirements are satisfied and have the following additional requirements:

- No events overlap.
- Every event from the original list is still present.

Events will have the following format:

`<start_date> -> <end_date> - <event_name>`

Where:

`<start_date>, <end_date>: YYYY/MM/DD HH:mm`

`<event_name>: Any valid character including spaces`

**Example input**:

`2022/08/23 15:00 -> 2022/08/23 16:00 - Meet Jamie for coffee`

`2022/08/23 16:15 -> 2022/08/23 17:00 - Guitar lessons`

If you do not have time to handle all possible scenarios, an app which handles a subset of them correctly is better than one which does not run or fails all requirements. For example, instead of re-scheduling events that overlap, keep the first event that was provided and drop any others that overlap with it.

You will be asked to extend the solution with additional features during the next interview stage.

You should see your Tech Lead as a member of the team you are handing the project over to. Please provide everything you feel would be relevant for them to easily review and potentially develop further without you. This might include tests, a README, and instructions for how to run your project in a clean OS X/Linux environment.

## What is the Scheduler?
The Scheduler is a CLI tool for re-adjusting a schedule so that all the events fit within Mon-Fri 0900-1800 without overlapping. The Scheduler will open an editor to put all events in (as well as advising on the format they have to be in) and then echos the response back of the events in order and correctly scheduled.

It first filters the list down to only valid events, prioritising overlaps by the first encountered event. Afterwards we try to re-insert the invalid ones back into the schedule in a greedy fashion; choosing to pick as immediately after its original start time as possible as per the stated requirements. 

## Are there any potential improvements?
There are possibly other more optimal ways of performing the scheduling to pack the schedule in more densely:
 - considering both earlier and afterwards when slotting events back in
 - by doing a re-prioritisation of both valid and invalid events based on duration to see what could fit better within a single day

But from the requirements we can't yet determine any form of priority to optimise for, so it would be good to find out more info on what the user really needs from this tool.

It is also written more so for clarity (making clear first and second passes, choosing to use a double for-loop O(n<sup>2</sup>) method for determining overlaps and for re-inserting events) and using traits of pure functional programming (immutability of lists, for example) than pure performance, so with quite a number of events this could end up taking more time. If performance were an issue, we could try to remove the redundant iteration and making more use of each pass to do more.

## How to run the Scheduler
1. Create and activate a virtual environment (instructions for `venv` [here](https://realpython.com/python-virtual-environments-a-primer/#create-it), or you can pick your own)
2. Run `pip install -r requirements.txt`
3. Run `python ./src/main.py`

## Tests
There are unit tests written using pytest. Given time constraints I've specifically picked to write tests for certain complex functions that prove out the majority of the logic in the process rather than everything.

To run them simply run `pytest` from the project root.
