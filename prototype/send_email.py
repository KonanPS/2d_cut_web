import mandrill

API_KEY = '80KloY055Hmqf61tLbPlEA'

try:
    mandrill_client = mandrill.Mandrill(API_KEY)

    message = {
     'auto_html': None,
     'auto_text': None,
     'from_email': 'cut@XN--7---7CD0AK0BPOGT7J.XN--P1AI',
     'from_name': 'Best cut',
     'headers': {'Reply-To': 'cut@XN--7---7CD0AK0BPOGT7J.XN--P1AI'},
     'html': '<p>Example HTML content</p>',
     'merge_language': 'mailchimp',
     'subject': 'Results',
     'tags': ['calculation-results'],
     'text': 'Example text content',
     'to': [{'email': 'konan.ps@gmail.com',
             'name': 'Pavel',
             'type': 'to'}],
     'track_clicks': None,
     'track_opens': 1,
     'tracking_domain': None,
     'url_strip_qs': None,
     'view_content_link': None}
    result = mandrill_client.messages.send(message=message, async=False, ip_pool='Main Pool')

except mandrill.Error, e:
    # Mandrill errors are thrown as exceptions
    print 'A mandrill error occurred: %s - %s' % (e.__class__, e)

