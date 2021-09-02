# Insta_Hashtag_PBFS
Python script that does a Prioritized Breadth First Search on a Hashtag using Instagram Graph API to find related and High traffic/growth hashtags from the root hashtag.

Create a facebook app from [developers.facebook](https://developers.facebook.com/) and add necessary permissons, then insert **Your Access Token and Instagram ID** *(not username)* in the script.

![Alt text](https://github.com/rishabhaskar2304/Insta_Hashtag_PBFS/blob/main/Screenshot%20(6).png)

P.S. - By default the script will only request 1 node(*Hashtag*) because of API limitations of Instagram Graph API which is 
> You can query a maximum of 30 unique hashtags within a 7 day period.

and that is exactly why the Breadth-First-Search has to be prioritized for better results.
But you can change `api_call_limit` variable in the script according to yourneed and weekly limit left.

I have equally distributed priority contribution among likes associated with each hashtag, number of occurences of the hashtag and minimum rank(position of hashtag in the top-media page) in the search.


```  vct[3]+= float(vct[0]/mxoc) + float(vct[1]/mxlk) + 1.0 - float(vct[2]/25)  ```


I would like to thank [Justin Stolpe](https://github.com/jstolpe) for his amazing [videos](https://www.youtube.com/c/justinstolpe/playlists).
