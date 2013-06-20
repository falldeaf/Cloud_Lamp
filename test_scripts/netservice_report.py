import imaplib, re
conn = imaplib.IMAP4_SSL("imap.gmail.com", 993)
conn.login('falldeaf@gmail.com', 'qxxunaqcwvjpbopk')
unreadCount = re.search("UNSEEN (\d+)", conn.status("INBOX", "(UNSEEN)")[1][0]).group(1)
print unreadCount
