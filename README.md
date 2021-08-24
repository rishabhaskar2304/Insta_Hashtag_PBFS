# Insta_Hashtag_PBFS
Python script that does a Priority Breadth First Search on a Hashtag using Instagram Graph API.

Create a facebook app from [developers.facebook](https://developers.facebook.com/) and add necessary permissons, then insert **Your Access Token and Instagram ID** *(not username)* in the script.

![Alt text](https://github.com/rishabhaskar2304/Insta_Hashtag_PBFS/blob/main/Screenshot%20(6).png)

P.S. - By default the script will only request 1 node(*Hashtag*) because of API limitations of Instagram Graph API which is 
> You can query a maximum of 30 unique hashtags within a 7 day period.

This is exactly why the search has to be prioritized.
But you can change `api_call_limit` variable in the script according to yourself.

I would like to thank [Justin Stolpe](https://github.com/jstolpe) for his amazing [videos](https://www.youtube.com/c/justinstolpe/playlists).
