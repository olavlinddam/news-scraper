It could also be like this maybe:

1. news_service returns news_dtos to the controller.
2. subscription_service returns subscribers to the controller.
3. controller send subscribers to the notification_service, so it has an in memory list of subscribers.
4. controller sends news_dtos to the redis_service.
5. redis_service publishes to any subscribers (in a queue style so the subscriber sets the pace)
6. notification_service subscribes to the queue in the redis_service and it publishes messages to the clients that are subscribing to new news (here i mean any client, like an app or browser extension, that are subscribing to my webhook). 

step 2-3 should only happen if there have been any new subscribers since the last run 
