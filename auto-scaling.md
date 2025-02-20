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



---------------------------------------------------------------------------------------


🔹 Adjusting the Script to Incrementally Scale Up
If you want to add more instances each time instead of setting a fixed number, modify the script like this:

#!/bin/bash

SERVICE_NAME="django-test-stack_django"
THRESHOLD=70  # CPU foizi
MAX_REPLICAS=10  # Maksimal xizmat nusxalari
MIN_REPLICAS=2   # Minimal xizmat nusxalari
SCALE_STEP=1  # Har safar qo‘shiladigan nusxa soni

while true; do
    CPU_LOAD=$(docker stats --no-stream --format "{{.CPUPerc}}" $(docker ps -q) | awk '{sum+=$1} END {print sum}')
    CURRENT_REPLICAS=$(docker service ls | grep $SERVICE_NAME | awk '{print $4}' | cut -d "/" -f 1)
    
    if (( $(echo "$CPU_LOAD > $THRESHOLD" | bc -l) )); then
        NEW_REPLICAS=$((CURRENT_REPLICAS + SCALE_STEP))
        if [ $NEW_REPLICAS -le $MAX_REPLICAS ]; then
            echo "CPU yuqori ($CPU_LOAD%), xizmatni kengaytirish: $CURRENT_REPLICAS → $NEW_REPLICAS"
            docker service scale $SERVICE_NAME=$NEW_REPLICAS
        fi
    elif (( $(echo "$CPU_LOAD < 30" | bc -l) )); then
        NEW_REPLICAS=$((CURRENT_REPLICAS - SCALE_STEP))
        if [ $NEW_REPLICAS -ge $MIN_REPLICAS ]; then
            echo "CPU past ($CPU_LOAD%), xizmat nusxalarini kamaytirish: $CURRENT_REPLICAS → $NEW_REPLICAS"
            docker service scale $SERVICE_NAME=$NEW_REPLICAS
        fi
    fi
    
    sleep 30  # 30 soniyada bir tekshiradi
done



🔹 How This Works:
Checks the current replica count.
If CPU usage > 70%, increases replicas by +1 (up to MAX_REPLICAS=10).
If CPU usage < 30%, decreases replicas by -1 (down to MIN_REPLICAS=2).
Ensures it does not exceed the max or drop below the minimum.


🚀 Final Answer
docker service scale django-test-stack_django=5 sets the total to 5, not adds 5.
If you need incremental scaling, modify the script as shown above.
Would you like to fine-tune it further? 😊