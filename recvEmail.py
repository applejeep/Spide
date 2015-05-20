#-*-coding:utf-8 -*-
import poplib
import email
from email.parser import Parser
from email.header import decode_header
from email.utils import parseaddr
#文本邮件的内容也是str，还需要检测编码，否则，非UTF-8编码的邮件都无法正常显示：
def guess_charset(msg):
    charset = msg.get_charset()# 先从msg对象获取编码:
    if charset is None:   # 如果获取不到，再从Content-Type字段获取:
        content_type = msg.get('Content-Type', '').lower()
        pos = content_type.find('charset=')
        if pos >= 0:
            charset = content_type[pos + 8:].strip()
    return charset
#邮件的Subject或者Email中包含的名字都是经过编码后的str，要正常显示，就必须decode：
def decode_str(s):
    value, charset = decode_header(s)[0]#decode_header()返回一个list，因为像Cc、Bcc这样的字段可能包含多个邮件地址，所以解析出来的会有多个元素,这里测试只取第一个
    if charset:
        value = value.decode(charset)
    return value
#但是这个Message对象本身可能是一个MIMEMultipart对象，即包含嵌套的其他MIMEBase对象，嵌套可能还不止一层。所以我们要递归地打印出Message对象的层次结构：
def print_info(msg, indent=0):#indent打印缩进
    if indent == 0:
        for header in ['From', 'To', 'Subject']:   # 邮件的From, To, Subject存在于根对象上:
            value = msg.get(header, '')
            if value:
                if header=='Subject':   # 需要解码Subject字符串:
                    value = decode_str(value)
                else:
                    hdr, addr = parseaddr(value)   # 需要解码Email地址:
                    name = decode_str(hdr)
                    value = u'%s <%s>' % (name, addr)
            print('%s%s: %s' % ('  ' * indent, header, value))
    if (msg.is_multipart()):   # 如果邮件对象是一个MIMEMultipart,  # get_payload()返回list，包含所有的子对象:
        parts = msg.get_payload()
        for n, part in enumerate(parts):
            print('%spart %s' % ('  ' * indent, n))
            print('%s--------------------' % ('  ' * indent))
            print_info(part, indent + 1)  # 递归打印每一个子对象:
    else:
         # 邮件对象不是一个MIMEMultipart,
        # 就根据content_type判断:
        content_type = msg.get_content_type()
        if content_type=='text/plain' or content_type=='text/html': # 纯文本或HTML内容:
            content = msg.get_payload(decode=True)
            charset = guess_charset(msg)    # 要检测文本编码:
            if charset:
                content = content.decode(charset)
            print('%sText: %s' % ('  ' * indent, content + '...'))
        else:  # 不是文本,作为附件处理:
            print('%sAttachment: %s' % ('  ' * indent, content_type))
email = raw_input('Email: ')
password =raw_input('Password: ')
pop3_server =raw_input('POP3 server: ') #网易 pop3.163.com
server = poplib.POP3(pop3_server)
#server.set_debuglevel(1)
print(server.getwelcome())
# 认证:
server.user(email)
server.pass_(password)
print('Messages: %s. Size: %s' % server.stat())
resp, mails, octets = server.list()
# 获取最新一封邮件, 注意索引号从1开始:
#resp, lines, octets = server.retr(len(mails))
resp, lines, octets = server.retr(6)
# 解析邮件:
msg = Parser().parsestr('\r\n'.join(lines))
# 打印邮件内容:
print_info(msg)
# 慎重:将直接从服务器删除邮件:
# server.dele(len(mails))
# 关闭连接:
server.quit()

