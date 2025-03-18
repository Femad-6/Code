#include <semaphore.h>
#include <pthread.h>
#include <time.h>
#include <unistd.h>
#include <iostream>
#include <queue>

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
        srand(time(0));
        /* sleep(rand() % 3 + 2); */
        sleep(3);
    }
}

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
        cout << "第" << i << "位顾客来了，正在接受理发师的理发服务" << endl;
        cout << "正在等待理发师理发的顾客还有" << waiting << "位" << endl
             << endl;
    }
    else
    {
        sem_post(&mutexlock);
        cout << "门外的第" << i << "位顾客看见没有椅子就转身走了" << endl
             << endl;
    }

    pthread_exit(0);
}

int main()
{
    pthread_t p_barber;
    pthread_t p_consumers[10];

    int num_consumers = 20;

    sem_init(&barber, 0, 0);
    sem_init(&consumers, 0, 0);
    sem_init(&mutexlock, 0, 1);

    pthread_create(&p_barber, nullptr, barber_process, nullptr);

    for (int i = 0; i < num_consumers; i++)
    {
        pthread_create(&p_consumers[i], nullptr, consumer_process, &i);
        srand(time(0));
        sleep(rand() % 2 + 1);
    }

    for (int i = 0; i < num_consumers; i++)
    {
        pthread_join(p_consumers[i], nullptr);
    }

    sleep(5);

    return 0;
}
