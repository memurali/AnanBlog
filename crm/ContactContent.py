from base.models import ContactUs

def getContact(fetch_amount, page):

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
                        <td>First Name</td>
                        <td>Last Name</td>
                        <td>E-mail</td>
                        <td>Phone</td>
                        <td>Consultation</td>
                        <td>Company Name</td>
                        <td>Additional Details</td>
                        <td>Message</td>
                        <td>Relevant File</td>
                    </tr>
                </thead>

        """

        for contact in contacts:

            x += f"""
            
                <tbody>

                    <tr>

                        <td><a class="text-info" href="customer/{contact.id}">{contact.firstName}</a></td>
                        <td>{contact.lastName}</td>
                        <td>{contact.email}</td>
                        <td>{contact.phone}</td>
                        <td>{contact.consultation}</td>
                        <td>{contact.companyName}</td>
                        <td>{contact.message}</td>
                        <td>{contact.additionalDetails}</td>
                """

            
            if contact.relevantFile == 'False':
                x += """
                
                    <td></td>
                
                """
            else:
                x += f"""
                
                    <td><a target="blank" class="text-primary" href="{contact.relevantFile.url}"> Attached File </a></td>

                """
            
            x += """
                    </tr>

                </tbody>
            
            """

        x += "</table>"

        x += z

        return x