import pandas as pd
from datetime import datetime, timedelta

# قراءة الملف
file_path = 'UAV_Rot.csv'
df = pd.read_csv(file_path)

# تجربة استخدام تنسيق "ISO8601"
try:
    df['time'] = pd.to_datetime(df['time'], format='%m/%d/%Y %H:%M', errors='raise')
except ValueError as e:
    print("ISO8601 format failed, trying mixed format.")
    df['time'] = pd.to_datetime(df['time'], format='ISO8601', errors='coerce')

# الحصول على الفروق الزمنية بين الصفوف
time_diffs = df['time'].diff().fillna(pd.Timedelta(seconds=0))

# بدء من وقت حالي
start_time = datetime.now()

# تطبيق الفروق الزمنية على الوقت الحالي لتحديث البيانات الزمنية
df['new_time'] = [start_time + sum(time_diffs[:i+1], timedelta()) for i in range(len(time_diffs))]

# إضافة عمود جديد باسم 'id' وملئه بالقيمة 'No.1'
df['id'] = 'No.1'

# حفظ الملف المحدث
new_file_path = 'updated_drone_data.csv'
df.to_csv(new_file_path, index=False)

print(f"Data has been updated and saved to {new_file_path}")
