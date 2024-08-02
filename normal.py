def is_leap_year(year):
    if (year % 4 == 0 and year % 100 != 0) or (year % 400 == 0):
        print(year , 'là năm nhuận') 
    else:
        print(year , ' không phải là năm nhuận') 


year = int(input('Nhập năm bất kỳ: '))
is_leap_year(year)