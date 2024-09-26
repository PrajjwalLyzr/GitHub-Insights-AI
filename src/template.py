def emailtemplate():
    email = """
                Dear {{ReceiverName}},\n
                Here are the top trending GitHub repositories for {{technology}} today\n

                {{Repository Name}}\n
                Description: {{Repository Description}}\n
                URL: {{Repository URL}}\n

                Best regards,\n
                Your AI Assistant"

            """
    
    return email

