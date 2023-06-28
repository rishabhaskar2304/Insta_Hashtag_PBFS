# Insta_Hashtag_PBFS
## Description
Developed an innovative Instagram Hashtag Recommendation Application utilizing the power of the Instagram Graph API. The application enables users to discover real-time, high-traffic generating, and relevant hashtags by inputting a single hashtag.

Implemented a Prioritized Breadth-First Search algorithm, leveraging the top media endpoint of the Instagram Graph API. By retrieving the top-ranking media posts for a given hashtag, calculated a priority based on factors such as likes, post rank, and hashtag occurrences. This priority determined the order of subsequent API calls, ensuring efficient exploration of the hashtag network.

In an ideal scenario, without API limitations, the application has the potential to generate a vast number of hashtags. With an estimation of 29 unique hashtags per post, multiplied by 50 top media posts, multiplied by the depth of the Prioritized Breadth-First Search tree (D), the possibilities are extensive.

I am excited about the impact this application can have on helping Instagram users optimize their hashtag usage and reach a wider audience. Feel free to explore the application and unlock a world of hashtag possibilities for your posts.

## Steps
Register a Facebook app on [developers.facebook](https://developers.facebook.com/) and add necessary permissions, then insert **Your Access Token and Instagram ID** *(not username)* in the script.

Dependencies : **openpyxl, re**

![Alt text](https://github.com/rishabhaskar2304/Insta_Hashtag_PBFS/blob/main/Screenshot%20(6).png)

P.S. - By default, the script will only request 1 node(*Hashtag*) because of API limitations of Instagram Graph API which is 
> You can query a maximum of 30 unique hashtags within a 7-day period.

and that is exactly why the Breadth-First-Search has to be prioritized for better results.
But you can change the `api_call_limit` variable in the script according to your need and the weekly limit left.
 
I have equally distributed priority contributions among likes associated with each hashtag, the number of occurrences of the hashtag, and minimum rank(position of the hashtag in the top-media page) in the search.


```  vct[3]+= float(vct[0]/mxoc) + float(vct[1]/mxlk) + 1.0 - float(vct[2]/25)  ```


I would like to thank [Justin Stolpe](https://github.com/jstolpe) for his amazing [videos](https://www.youtube.com/c/justinstolpe/playlists).

IEEE Research Paper on the topic: https://ieeexplore.ieee.org/document/9734217
