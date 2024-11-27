from base.models import ContactUs
from crm.models import *

def getAccount(fetch_amount, page):

    page = int(page)

    z = ""

    if fetch_amount == "all":

        cn = ContactUs.objects.all()

        cnt = 0

        if not cn:
            pass
        else:

            cnl = (len(cn) / 6) + 0.1

            if cnl <= 1:
                pass
            else:

                nxt_page = page + 1
                prev_page = page - 1

                if prev_page < 1:
                    prev_page = 1
                
                if nxt_page > round(cnl):
                    nxt_page = round(cnl)

                start = (page - 1) * 6
                end = page * 6

                cnt = 1

                z = f"""
                
                    <nav aria-label="Page navigation example">
                        <ul class="pagination">
                            <li class="page-item">
                                <a class="page-link" href="?page={prev_page}" aria-label="Previous">
                                    <span aria-hidden="true">&laquo;</span>
                                    <span class="sr-only">Previous</span>
                                </a>
                            </li>              
                """

                for c in range(round(cnl)):
                    c += 1
                    if c == page:
                        
                        z += f"""
                            <li class="page-item active"><a class="page-link" href="?page={c}">{c}</a></li>
                        
                        """
                    else:

                        z += f"""
                            <li class="page-item"><a class="page-link" href="?page={c}">{c}</a></li>
                        
                        """

                z += f"""
                
                    <li class="page-item">
                            <a class="page-link" href="?page={nxt_page}" aria-label="Next">
                                <span aria-hidden="true">&raquo;</span>
                                <span class="sr-only">Next</span>
                            </a>
                            </li>
                        </ul>
                    </nav>

                """

        if cnt == 0:
            contacts = ContactUs.objects.all().order_by("-id")
        else:
            contacts = ContactUs.objects.all().order_by("-id")[start:end]
    
    elif fetch_amount.isdigit == True:
        contacts = ContactUs.objects.all().order_by("-id")[:fetch_amount]
    else:
        contacts = ContactUs.objects.all().order_by("-id")[:5]

    if not contacts:
        return ""
    else:

        x = """
            <table class="table">
                <thead class=" text-primary">
                    <tr class="font-weight-bold">
                        <td>Name</td>
                        <td>Leads</td>
                        <td>Organization</td>
                        <td>E-mail</td>
                        <td>Phone</td>
                    </tr>
                </thead>

        """

        for contact in contacts:

            x += f"""
            
                <tbody>

                    <tr>

                        <td><a class="text-info" href="customer/{contact.id}">{contact.firstName} {contact.lastName}</a></td>
                        <td>{contact.source}</td>
                        <td>{contact.companyName}</td>
                        <td><input class="form-control bg-midnight" type="text" readonly value="{contact.email}"></td>
                        <td><input class="form-control bg-midnight" type="text" readonly value="{contact.phone}"></td>

                    </tr>

                </tbody>
            
            """

        x += "</table>"

        x += z

        return x


def getMessages(id):

    allMssg = SentMessage.objects.filter(contact_id=id)

    if not allMssg:
        return ""
    else:

        x = """
            <table class="table">
                <thead class=" text-primary">
                    <tr class="font-weight-bold">
                        <td>email</td>
                        <td>subject</td>
                        <td>message</td>
                        <td>sent time</td>
                    </tr>
                </thead>

        """

        for msg in allMssg:

            x += f"""
            
                <tr>
                    <td>{msg.to_email}</td>
                    <td>{msg.subject}</td>
                    <td>{msg.message}</td>
                    <td>{msg.cratedAt}</td>
                </tr>
            
            """

        x += "</table>"

        return x



def getActivities(id):

    activities = Activities.objects.filter(contact_id=id)

    if not activities:
        return ""
    else:

        x = """
            <table class="table">
                <thead class=" text-primary">
                    <tr class="font-weight-bold">
                        <td>activity</td>
                        <td>title</td>
                        <td>description</td>
                        <td>schedule</td>
                        <td>done</td>
                    </tr>
                </thead>

        """

        for msg in activities:

            if msg.activity == 'email':
                color = "activity_email"
            elif msg.activity == 'call':
                color = "activity_call"
            elif msg.activity == 'invoice':
                color = "activity_invoice"
            elif msg.activity == 'others':
                color = "activity_other"

            x += f"""
            
                <tr>
                    <td><span class="{color}">{msg.activity}</span></td>
                    <td>{msg.title}</td>
                    <td>{msg.description}</td>
                    <td>{msg.schedule}</td>
            """
            
            if msg.done == True:

                x += """
                    <td>
                        <span class="green-check">
                        <i class="material-icons">check</i>
                        </span>
                    </td>
                    </tr>
                
                """
            else:

                x += """
                    <td>
                        <span class="red-check">
                        <i class="material-icons">clear</i>
                        </span>
                    </td>
                    </tr>
                
                """


        x += "</table>"

        return x