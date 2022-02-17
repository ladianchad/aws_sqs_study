import sqs

if __name__ == "__main__":
    manager =  sqs.SqsManger(
        
    )
    print(manager)
    print(manager.get())
