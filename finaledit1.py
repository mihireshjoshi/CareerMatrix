from fpdf import FPDF

class PDF(FPDF):
    def header(self):
        if self.page_no() == 1:  # Check if it's the front page
            self.set_font('Arial', 'B', 18)
            self.cell(0, 10, 'RESUME', 0, 1, 'C')

    # def footer(self):
    #     self.set_y(-15)
    #     self.set_font('Arial', 'I', 8)
    #     self.cell(0, 10, f'Page {self.page_no()}', 0, 0, 'C')

    def add_section(self, title):
        self.set_font('Arial', 'B', 14)
        self.cell(0, 10, title, 0, 1, 'L')
        self.ln(5)

    def add_content(self, content):
        self.set_font('Arial', '', 12)
        self.multi_cell(0, 10, content)
        self.ln(5)

    def add_table(self, header, data):
        col_widths = [70, 100]  # Adjust column widths as needed
        self.set_fill_color(200, 220, 255)  # Light blue background for header row
        self.set_text_color(0)  # Black text color
        self.set_font('Arial', 'B', 12)
        for header_item in header:
            self.cell(col_widths[header.index(header_item)], 10, header_item, 1, 0, 'C', 1)
        self.ln()
        
        # Alternating row colors for better readability
        fill = False
        for row in data:
            self.set_fill_color(255, 255, 255) if fill else self.set_fill_color(240, 240, 240)
            fill = not fill
            self.set_text_color(0)  # Black text color
            self.set_font('Arial', '', 12)
            for item in row:
                self.cell(col_widths[row.index(item)], 10, item, 1, 0, 'L', 1)
            self.ln()

# Create instance of FPDF class
pdf = PDF()

# Add a page
pdf.add_page()

# Input from user for personal information
personal_info = {}
personal_info['Name'] = input("Enter your name: ")
personal_info['Email'] = input("Enter your email: ")
personal_info['Phone'] = input("Enter your phone number: ")
personal_info['LinkedIn'] = input("Enter your LinkedIn profile URL: ")
personal_info['GitHub'] = input("Enter your GitHub profile URL: ")

# Add content to the PDF
pdf.set_font('Arial', 'B', 16)
pdf.add_section('Personal Information')
for key, value in personal_info.items():
    pdf.add_content(f'{key}: {value}')

# Input from user for qualifications
qualifications = []
while True:
    degree = input("Enter your degree (or leave blank to finish): ")
    if not degree:
        break
    details = input("Enter details of the degree: ")
    qualifications.append([degree, details])

pdf.add_section('Qualifications')
pdf.add_table(['Degree', 'Details'], qualifications)

# Input from user for internships
internships = []
while True:
    role = input("Enter your role during the internship (or leave blank to finish): ")
    if not role:
        break
    company = input("Enter the company name: ")
    duration = input("Enter the duration of the internship: ")
    internships.append(['Role', role])
    internships.append(['Company', company])
    internships.append(['Duration', duration])

pdf.add_section('Internships')
pdf.add_table(['Attribute', 'Details'], internships)

# Input from user for projects
projects = []
while True:
    project = input("Enter the name of the project (or leave blank to finish): ")
    if not project:
        break
    year = input("Enter the year of the project: ")
    projects.append(['Project', project])
    projects.append(['Year', year])

pdf.add_section('Projects')
pdf.add_table(['Attribute', 'Details'], projects)

# Input from user for awards
awards = []
while True:
    award = input("Enter the name of the award (or leave blank to finish): ")
    if not award:
        break
    organization = input("Enter the organization granting the award: ")
    year = input("Enter the year of the award: ")
    awards.append(['Award', award])
    awards.append(['Organization', organization])
    awards.append(['Year', year])

pdf.add_section('Awards')
pdf.add_table(['Attribute', 'Details'], awards)

# Save the PDF to a file
pdf_file = "comprehensive_resume.pdf"
pdf.output(pdf_file)

print(f"PDF generated: {pdf_file}")
