#include <iostream>
#include <vector>
#include <algorithm>
using namespace std;

struct Job {
    int id;
    int burstTime;
    int priority;
};

// FCFS
void scheduleFCFS(const vector<Job>& jobs) {
    int n = jobs.size();
    vector<int> wt(n), tat(n);
    wt[0] = 0;
    for (int i = 1; i < n; i++)
        wt[i] = wt[i - 1] + jobs[i - 1].burstTime;
    for (int i = 0; i < n; i++)
        tat[i] = wt[i] + jobs[i].burstTime;

    double sumWT = 0, sumTAT = 0;
    cout << "Job ID\tBurst\tWaiting\tTurnaround\n";
    for (int i = 0; i < n; i++) {
        sumWT  += wt[i];
        sumTAT += tat[i];
        cout << jobs[i].id << "\t"
             << jobs[i].burstTime << "\t"
             << wt[i] << "\t"
             << tat[i] << "\n";
    }
    cout << "Avg WT: " << (sumWT / n)
         << "    Avg TAT: " << (sumTAT / n) << "\n";
}

// SJF
bool compareSJF(const Job &a, const Job &b) {
    return a.burstTime < b.burstTime;
}

void scheduleSJF(vector<Job> jobs) {
    sort(jobs.begin(), jobs.end(), compareSJF);
    scheduleFCFS(jobs);
}

// PRIORITY
bool comparePriority(const Job &a, const Job &b) {
    return a.priority < b.priority;
}

void schedulePriority(vector<Job> jobs) {
    sort(jobs.begin(), jobs.end(), comparePriority);
    scheduleFCFS(jobs);
}

// RR
void scheduleRoundRobin(const vector<Job>& jobs, int quantum) {
    int n = jobs.size();
    vector<int> bt(n), wt(n), tat(n);
    for (int i = 0; i < n; i++)
        bt[i] = jobs[i].burstTime;

    int t = 0;
    bool done;
    do {
        done = true;
        for (int i = 0; i < n; i++) {
            if (bt[i] > 0) {
                done = false;
                if (bt[i] > quantum) {
                    t += quantum;
                    bt[i] -= quantum;
                } else {
                    t += bt[i];
                    wt[i] = t - jobs[i].burstTime;
                    bt[i] = 0;
                }
            }
        }
    } while (!done);

    for (int i = 0; i < n; i++)
        tat[i] = jobs[i].burstTime + wt[i];

    double sumWT = 0, sumTAT = 0;
    cout << "Job ID\tBurst\tWaiting\tTurnaround\n";
    for (int i = 0; i < n; i++) {
        sumWT  += wt[i];
        sumTAT += tat[i];
        cout << jobs[i].id << "\t"
             << jobs[i].burstTime << "\t"
             << wt[i] << "\t"
             << tat[i] << "\n";
    }
    cout << "Avg WT: "  << (sumWT  / n)
         << "    Avg TAT: " << (sumTAT / n) << "\n";
}

int main() {
    int n;
    if (!(cin >> n)) return 0;

    vector<Job> jobs(n);
    for (int i = 0; i < n; i++) {
        jobs[i].id = i + 1;
        cin >> jobs[i].burstTime >> jobs[i].priority;
    }

    int choice;
    cin >> choice;

    switch (choice) {
        case 1: scheduleFCFS(jobs);        break;
        case 2: scheduleSJF(jobs);         break;
        case 3: schedulePriority(jobs);    break;
        case 4: {
            int quantum;
            cin >> quantum;
            scheduleRoundRobin(jobs, quantum);
            break;
        }
        default:
            cerr << "Invalid choice\n";
    }

    return 0;
}
