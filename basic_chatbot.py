#Simple Chatbot

hello_greet = ['hi', 'Hi', 'HI', "hI"]

count = 5

print("Hello, my name is JANET\nPrompts:")
print("1) who are you\n2) how are you\n3) will you marry me\n")

for i in range(5):

    print(f"Remaining number of things you can ask JANET: {count}\n")
    user_input = input("You: ")

    if user_input in hello_greet:
        print('JANET: Hi, How can I help you?')
    elif user_input == 'who are you':
        print('JANET: I am your chatbot.... Do you remember me?\n')

        remember = input('Response: ')
        yes_greet = ['yes', 'yeS', 'yES','YES', 'yEs', 'Yes', 'YEs', 'YeS']
        no_greet = ['no', 'NO','nO', 'No']
        if remember in yes_greet:
            print('Oh ok. Great to hear.')
        elif remember in no_greet:
            print('That\'s alright. My name is JANET. Nice to meet you.')
        else:
            print('Je ne comprends pas maintenant. Je suis desolé.')

    elif user_input == 'how are you':
        print('JANET: I am doing well. Thank you for asking!\n')
    elif user_input == 'will you marry me':
        print('JANET: I cannot comprehend the feeling of love. I appreciate the gesture though.\n')
    else:
        print('I am sorry. I did not understand what you said.\n')

    count-=1

print("\nThank you for asking questions! I greatly appreciated your time!")
