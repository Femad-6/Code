#include <semaphore.h>
#include <pthread.h>
#include <time.h>
#include <unistd.h>
#include <iostream>
#include <queue>
#include <vector>
#include <algorithm>
#include <ctime>
#include <cstdlib>
#include <cstdio>

using namespace std;

typedef sem_t semaphore;
queue<int> wait_queue;

#define CHAIRS 5
int waiting = 0;

semaphore barber;
semaphore consumers;
semaphore mutexlock;

void *barber_process(void *)
{
    while (1)
    {
        int id;
        sem_wait(&consumers);
        sem_wait(&mutexlock);
        waiting = waiting - 1;
        id = wait_queue.front();
        wait_queue.pop();
        sem_post(&barber);
        sem_post(&mutexlock);
        cout << "理发师正在给第" << id << "位等待的顾客理发" << endl;
        sleep(rand() % 3 + 2); // 取消注释并替换固定值
    }
}

// 在全局变量区域添加
pthread_mutex_t print_mutex = PTHREAD_MUTEX_INITIALIZER;

void *consumer_process(void *p)
{
    int i = *(int *)p;
    sem_wait(&mutexlock);
    if (waiting < CHAIRS)
    {
        wait_queue.push(i);
        waiting = waiting + 1;
        sem_post(&consumers);
        sem_post(&mutexlock);
        sem_wait(&barber);
        pthread_mutex_lock(&print_mutex);
        cout << "第" << i << "位顾客来了，正在接受理发师的理发服务" << endl;
        cout << "正在等待理发师理发的顾客还有" << waiting << "位" << endl
             << endl;
        pthread_mutex_unlock(&print_mutex);
    }
    else
    {
        sem_post(&mutexlock);
        cout << "门外的第" << i << "位顾客看见没有椅子就转身走了" << endl
             << endl;
    }

    pthread_exit(0);
    return NULL;
}

int main()
{
    srand(time(0)); // 移到主函数开头，只初始化一次

    pthread_t p_barber;
    pthread_t p_consumers[20];
    int customer_ids[20]; // 新增顾客ID数组

    int num_consumers = 20;

    sem_init(&barber, 0, 0);
    sem_init(&consumers, 0, 0);
    sem_init(&mutexlock, 0, 1);

    pthread_create(&p_barber, NULL, barber_process, NULL);

    for (int i = 0; i < num_consumers; i++)
    {
        customer_ids[i] = i + 1; // 为每个顾客分配唯一ID
        pthread_create(&p_consumers[i], NULL, consumer_process, &customer_ids[i]);
        srand(time(0));
        sleep(rand() % 2 + 1);
    }

    for (int i = 0; i < num_consumers; i++)
    {
        pthread_join(p_consumers[i], NULL);
    }

    sleep(5);

    return 0;
}
// 用dev-c++编译通过
