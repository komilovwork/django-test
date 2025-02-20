🚀 Docker Swarm va AutoScaling: Xizmatlarni Avtomatik Ko‘paytirish
Docker Swarm o‘z-o‘zidan avtomatik autoscaling qilmaydi. Ammo CPU yoki RAM yuklanishiga qarab xizmatlarni qo‘lda autoscale qilish mumkin.

📌 Docker Swarm-da Autoscaling qanday ishlaydi?
Docker Swarm o‘z-o‘zidan yukni taqsimlaydi, lekin u xizmatlarni avtomatik ravishda ko‘paytirib yoki kamaytirib bera olmaydi.
Shuning uchun, autoscaling qo‘shish uchun quyidagi usullardan birini ishlatish mumkin:

1️⃣ Qo‘lda Autoscaling:

docker service scale buyrug‘i yordamida xizmatlar sonini oshirish/ kamaytirish.
Masalan, Django`ning 2 ta nusxasi o‘rniga 5 ta qilish.
2️⃣ CPU & RAM Monitoring + Autoscaling Skripti (Tavsiya etiladi):

CPU yoki RAM muayyan chegaradan oshganda, yangi konteynerlar qo‘shish.
Prometheus + Alertmanager + Swarm API yoki Docker Events yordamida avtomatlashtirish.
3️⃣ Docker Swarm-ning Load Balancing Imkoniyati:

Docker Swarm yukni avtomatik taqsimlaydi, ya’ni yangi so‘rovlar mavjud xizmatlar orasida taqsimlanadi.
Ammo yangi nusxalarni avtomatik qo‘shib bermaydi.
✅ 1-Usul: Qo‘lda AutoScaling (docker service scale)
Agar siz Swarm Cluster ichida xizmatlar sonini oshirmoqchi bo‘lsangiz, quyidagi buyruqni ishlatish kifoya:

sh

docker service scale django-test-stack_django=5

🔹 Bu nima qiladi?

Django xizmatining 5 ta konteyner nusxasini ishga tushiradi.
Swarm yangi kelgan so‘rovlarni ushbu 5 ta konteyner orasida taqsimlaydi.
Agar ma’lumotlar bazasiga yuk oshsa, PostgreSQL xizmatini ham kengaytirish mumkin:

sh

docker service scale django-test-stack_db=3

Cheklovlari:

Qo‘lda bajarish kerak.
Avtomatik yuklanishga javob bermaydi.
✅ 2-Usul: CPU/RAM Monitoring + Avtomatik Scaling Skripti
Agar siz avtomatik autoscaling qilishni xohlasangiz, CPU yoki RAM yuklanishini kuzatish va kerak bo‘lsa xizmatlar sonini oshirish kerak.

🔹 Bash skript yordamida Autoscaling
Quyidagi skript har 30 soniyada CPU yuklanishini tekshiradi va agar 70% dan oshsa, xizmat nusxalarini ko‘paytiradi.

sh

#!/bin/bash

SERVICE_NAME="django-test-stack_django"
THRESHOLD=70  # CPU foizi
SCALE_UP=5     # Maksimal xizmat nusxalari
SCALE_DOWN=2   # Minimal xizmat nusxalari

while true; do
    CPU_LOAD=$(docker stats --no-stream --format "{{.CPUPerc}}" $(docker ps -q) | awk '{sum+=$1} END {print sum}')
    
    if (( $(echo "$CPU_LOAD > $THRESHOLD" | bc -l) )); then
        echo "CPU yuqori ($CPU_LOAD%), xizmatni kengaytirish..."
        docker service scale $SERVICE_NAME=$SCALE_UP
    elif (( $(echo "$CPU_LOAD < 30" | bc -l) )); then
        echo "CPU past ($CPU_LOAD%), xizmat nusxalarini kamaytirish..."
        docker service scale $SERVICE_NAME=$SCALE_DOWN
    fi
    
    sleep 30  # 30 soniyada bir tekshiradi
done


🔹 Bu nima qiladi?

Agar CPU yuklanishi 70% dan oshsa, xizmat 5 ta nusxaga oshadi.
Agar CPU yuklanishi 30% dan pastga tushsa, xizmat 2 ta nusxaga kamayadi.
📌 Buni ishlatish uchun skriptni serverga saqlang va ishga tushiring:

sh

chmod +x autoscale.sh
./autoscale.sh


Agar bu doimiy ishlashini xohlasangiz, Systemd yoki CronJob ga qo‘shish mumkin.

✅ 3-Usul: Prometheus + Alertmanager + Docker API
Bu murakkab, ammo eng optimal yechim bo‘lib, Prometheus monitoring tizimi va Docker API dan foydalaniladi.

🔹 Ishlash prinsipi:
Prometheus → CPU, RAM yuklanishini o‘lchaydi.
Alertmanager → CPU yoki RAM 80% ga yetganda trigger beradi.
Webhook orqali Docker API → xizmatni avtomatik kengaytiradi.
📌 Buni ishlatish uchun Prometheus monitoring tizimini o‘rnatish kerak.

🚀 Qaysi usulni tanlash kerak?
Usul	Afzalliklari	Kamchiliklari
Qo‘lda Scaling (docker service scale)	Oddiy, tez va oson	Qo‘lda bajarish kerak
Bash Skript bilan Avtomatik Scaling	Yengil avtomatlashtirish, CPU monitoring	Murakkab jarayon, hamma xizmatlarga mos emas
Prometheus + Alertmanager + Docker API	Eng optimal, avtomatik va ishonchli	Murakkab sozlash talab etadi
🎯 Xulosa
✅ Docker Swarm yukni avtomatik taqsimlaydi, lekin avtomatik autoscale qilmaydi.
✅ Qo‘lda docker service scale buyrug‘i bilan xizmatlarni kengaytirish mumkin.
✅ Bash skript yordamida CPU yukiga qarab avtomatik autoscaling qilish mumkin.
✅ Eng yaxshi usul: Prometheus + Alertmanager bilan avtomatik monitoring va scaling.

Agar siz tezkor va yengil yechim xohlasangiz, bash skriptni ishga tushiring.
Agar kattaroq, mustahkam avtomatlashtirish xohlasangiz, Prometheus Alertmanager bilan ishlang. 🚀

Qaysi usul siz uchun yaxshiroq? Fikr bildiring yoki savollaringiz bo‘lsa, so‘rashingiz mumkin! 😊