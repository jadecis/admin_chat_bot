import xlsxwriter
from loader import db 

workbook = xlsxwriter.Workbook('stat.xlsx')
worksheet = workbook.add_worksheet()
worksheet.write(f'A1', 'user_id')
worksheet.write(f'B1', 'username')
worksheet.write(f'C1', 'posts')
result= db.get_posts()
for i, j in enumerate(result, start=2):
    worksheet.write(f'A{i}', j[1])
    worksheet.write(f'B{i}', j[2])
    worksheet.write(f'C{i}', j[3])

workbook.close()
