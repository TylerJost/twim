# TWiA
*T*his *W*eek *i*n *A*ustin is meant to be a repository for code to make a playlist for upcoming artists in the Austin area. 

TWiA is also a curated playlist of songs from artists that are playing *this week (!!!)* in Austin, TX. 

Want to listen to the playlist? Check it out on Spotify at:
https://open.spotify.com/playlist/7oWlCMpyEMTjvu1GwIoDMN?si=38c25252b3054237

## How are the songs chosen?
Right now I'm taking the top 15 artists and including 3 songs per artist. The rest of the songs are 55 of the other artists' top songs at 1 song per artist. I think that 100 songs is already getting a little long for a playlist but this does pose a few other issues such as:

1. What to do about artists that are consistently playing? Artists that play in Austin every week need to be featured but they don't need to be in the running every week or day. There are simply too many people playing each week. I think this is a good problem! 

2. Should there be more than 100 songs?

3. Should it be more than just this week in Austin? Why not this month or just a daily playlist. 

Most of these problems are mainly up to your personal preference which is why *some* of the code is available. 

## How do you find the artists?
I scrape local with mostly plain-text interfaces to gather artists and the dates they are playing. This presents one big issue, which is how to deal with inconsistent ways of representing artists. For example, if a venue lists something such as:

 > Australian punk night presents: THE CHATS / COSMIC PSYCHOS / THE SCHIZOPHONICS

There are a few issues such as: 
- There's no band called "Australian punk night presents".
- Artists are all in caps.
- Artists are separated by "/".
- None of this is consistent and it could be different on another site. 

To remedy this I finetuned a BERT LLM to identify band names. Each artists also has to exist on Spotify. There are also a lot of repeat artists on Spotify/in the world and this makes it impossible to guarantee that I'm selecting the right artist. 

### I cannot gurantee that artists are correct!
There's just too many to ever manually verify, and pretty much any combination of words is somehow an existing artist on Spotify. 

**Note**: This is a bunch of spaghetti code for generating a playlist and is definitely a personal work in progress project. Stay tuned for updates!