package com.redeemerlives;

import com.amazonaws.services.lambda.runtime.Context;
import com.amazonaws.services.lambda.runtime.RequestHandler;
import com.amazonaws.services.lambda.runtime.events.S3Event;
import software.amazon.awssdk.services.sns.SnsClient;
import software.amazon.awssdk.services.sns.model.*;

public class EventDrivenArchitecture implements RequestHandler<S3Event, String> {

    private final SnsClient snsClient = SnsClient.create();
    private final String topicArn = System.getenv("SNS_TOPIC_ARN");

    @Override
    public String handleRequest(S3Event event, Context context) {
        String bucketName = event.getRecords().get(0).getS3().getBucket().getName();
        String objectKey = event.getRecords().get(0).getS3().getObject().getKey();

        String message = "New object uploaded: " + objectKey + " in bucket: " + bucketName;

        PublishRequest publishRequest = PublishRequest.builder()
                .topicArn(topicArn)
                .message(message)
                .subject("New Object Uploaded to S3")
                .build();

        snsClient.publish(publishRequest);

        return "Notification sent!";
    }
}
