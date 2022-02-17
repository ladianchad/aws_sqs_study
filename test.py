import sqs

if __name__ == "__main__":
    manager =  sqs.SqsManger(
        YOUR_REGION,
        AWS_ACCESS_KEY,
        AWS_ACCESS_PRIVATE,
        AWS_SQS_URL
    )
    print(manager)
    print(manager.get())
    manager.put("HELLO World")


