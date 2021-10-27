# The HearingRoom

## Description
The Hearing Room combines Symbl.ai and Machine Learning to create a catalogue of speaking points from videos of public figures.

Each person has a list of topics and links to time-stamped videos that go directly to where they spoke.

## Progress
For the scope of this project, we focused on the Senate Floor audio recordings archived at TVW.org - a website that offers "unedited coverage of Washington state government, politics and public policy".

Using a combination of Symbl.ai async audio API and facial identifier algorithm, we were able to accomplish the following:

Retrieve the transcript and topics from each media file through the Symbl.ai async audio API
Run a facial identifier algorithm to identify the people present in the media.
Run our stitching algorithm to analyze which faces belong to which senators.
Using the output from our stitch, we identified which speaker spoke about which topics per media file
Display the catalogued data on our website for users to browse. For example, if someone was interested in what topics Senator Rolfes had discussed, a user can navigate to her thumbnail, click on it, and it will show the list of topics she has talked about in the Senate Floor. Each topic has a list of link(s), which navigates the user to the moment of where the speaker talks about the topic in the video.
Concept
Our project aims to provide further resources for voters by listing what topics the incumbent candidates have discussed during their terms and link it back to the unedited coverage.

The voter's pamphlet is always sent out near the time of elections, which has some small summaries of the candidates. Sometimes we'd like to know if the topics we care about were discussed by the incumbent official, which may not be captured in the voter's pamphlet. Through our project, we conducted analyses on topics that were discussed, as well as facial recognition to connect the speakers to the topics, from the media files.

The Hearing Room is designed so that we can look up incumbents, find the topics they've discussed, and allow users to find a time-stamped video(s) of where they can hear the official talk about the topic.

## Feasibility
This project has ample rooms to grow in terms of information gathering to provide voters with easier access to the unedited coverage. Part of its growth involves, but not limited to, the following:

working with Symbl.ai to increase job processing as the trial we were using could only accommodate a max of 2 jobs at a time
expand coverage to other parts of the state government whose members are elected officials
identifying other sources from other states that provide unedited coverage of the government business that are open to the public for viewing
expanding it to the federal government level coverage (e.g. working with c-span)
Because a large part of the project's potential relies on automation, we estimate that over time the overhead operating cost to operate The Hearing Room will be significantly more efficient and productive compared to the initial setup.
