"""
Q : CAS (Compare And Swap) কী?
-> কম্পিউটার বিজ্ঞানে CAS (Compare And Swap) হলো প্রসেসর (CPU) বা Hardware লেভেলের একটি atomic নির্দেশ (instruction), যা মেমোরিতে থাকা
কোনো data নিরাপদভাবে update করার জন্য ব্যবহৃত হয়।

-> এতে তিনটি উপাদান থাকে:
1. Memory Location = যেখানে data রাখা আছে
2. Expected Value = আগে যে value-টি read করা হয়েছিল
3. New Value = যে new value-টি বসাতে চাই

-> যখন কোনো data update করার নির্দেশ দেওয়া হয়, তখন system প্রথমে Compare করে দেখে যে, মেমোরিতে থাকা বর্তমান value এবং প্রত্যাশিত value হুবহু
same আছে কি না।
 * যদি দুটি value same হয়, শুধুমাত্র তখনই নতুন value-টি সেখানে প্রতিস্থাপন (Swap) করা হয় এবং অপারেশনটি সফল হিসেবে গণ্য হয়।
 * যদি value same না হয়(অর্থাৎ মাঝখানে অন্য কেউ Data পরিবর্তন করে ফেলেছে), তবে কোনো পরিবর্তন হয় না এবং অপারেশনটি fail হিসেবে ফিরে আসে।

-> Atomicity
CAS হলো একটি "Atomic" প্রক্রিয়া। এর মানে হলো, "Compare" এবং "Swap"—এই দুটি কাজ একসাথে একটিমাত্র নিরবচ্ছিন্ন ধাপ হিসেবে execute হয়। এই
প্রক্রিয়ার ঠিক মাঝখানে অন্য কোনো Thread বা প্রক্রিয়া প্রবেশ করে data update করতে পারে না।
"""
import time

"""
Q : Optimistic Locking-এ CAS কেন প্রয়োজন?
-> এই বিষয়টি পরিষ্কারভাবে বোঝার জন্য একটি প্রচলিত সমস্যার কথা বিবেচনা করা যেতে পারে, যাকে বলা হয় "Race Condition" বা "Lost Update Problem"।

একটি ব্যাংক অ্যাকাউন্টের উদাহরণ দেওয়া হলো, যেখানে Balance আছে ১০০ টাকা। একই সময়ে দুটি ভিন্ন জায়গা (যেমন: Thread A এবং Thread B) থেকে 
অ্যাকাউন্টে ১০ টাকা করে জমা করার চেষ্টা করা হচ্ছে।
* Thread A: Data read করলো (১০০ টাকা)। ১০ টাকা যোগ করার জন্য new value prepare করলো (১১০ টাকা)।
* Thread B: ঠিক একই সময়ে Data read করলো (১০০ টাকা)। ১০ টাকা যোগ করার জন্য new value prepare করলো (১১০ টাকা)।

এখন যদি সাধারণ logic check (যেমন: if current_balance == 100) ব্যবহার করে data save করার চেষ্টা করা হয়, তবে একটি বিশাল সমস্যা হবে। 
Thread A যখন Balance Check করছে এবং ১১০ টাকা save করছে, ঠিক সেই fraction সেকেন্ডের মধ্যে thread B-ও একইভাবে check করে তার ১১০ 
টাকা save করে ফেলবে।
result কী দাঁড়াল? দুটি আলাদা save সত্ত্বেও Balance হলো ১১০ টাকা, অথচ হওয়া উচিত ছিল ১২০ টাকা। একটি update পুরোপুরি হারিয়ে গেল! কারণ সাধারণ 
if condition এবং value পরিবর্তন করার প্রক্রিয়াটি একসাথে কাজ করে না; এদের মাঝে কিছুটা সময়ের gap থাকে।

এই সমস্যার সমাধান দেয় CAS, Optimistic Locking-এর মূল নীতি হলো কাউকে Data ব্যবহারে বাধা না দেওয়া, কিন্তু comit করার সময় নিখুঁতভাবে 
validation করা। এই নিখুঁত validation-এর জন্যই CAS অপরিহার্য। CAS নিশ্চিত করে যে, Data check করা এবং update করার মাঝখানে অন্য কেউ 
ঢুকতে পারবে না।

Thread-A যখন CAS ব্যবহার করে ১১০ টাকা save করতে যাবে, তখন Hardware লেভেলে এক ধাপে check ও update সম্পন্ন হবে। Balance হয়ে যাবে ১১০।
এরপর Thread-B যখন নিজের ১১০ টাকা save করতে যাবে, তখন CAS দেখবে যে বর্তমান Balance আর ১০০ নেই। ফলে Thread B-এর Operation সাথে 
সাথে Fail হয়ে যাবে। এর ফলে ভুল Data save হওয়া প্রতিরোধ করা সম্ভব হয়।
"""


"""
-> CAS and Optimistic Locking
CAS Fail হলেও Transaction টি অসম্পূর্ণ রেখে দেওয়া যায় না। Fail হওয়ার মানে হলো Data-টি এই মুহূর্তে অন্য একটি transaction দ্বারা change হয়ে গেছে 
তাই latest Data নিয়ে কাজটি আবার করতে হবে। এই পুরো প্রক্রিয়াটি একটি automatic Loop-এর মাধ্যমে সম্পন্ন হয়।

নিচে ধাপে ধাপে একটি সম্পূর্ণ transaction-এর flow বর্ণনা করা হলো:

Step-1: Read Phase
প্রথমে Main Storage বা মেমোরি থেকে বর্তমান Value-টি পড়া হয়।
Value পাওয়া গেল: 5

Step-2: Preparation Phase
Read করা value-টির উপর ভিত্তি করে প্রয়োজনীয় processing সম্পন্ন করে নতুন একটি value তৈরি করা হয়।
হিসাব করা হলো: 5 + 1 = 6

Step-3: Validation Phase
এখন system-কে CAS command পাঠানো হয়। command-টি হয় এরকম: "মেমোরিতে যদি এখনও Value 5 থাকে, তবে সেটিকে পরিবর্তন করে 6 করো।"

Step-4: Retry Loop
এখানে দুটি ঘটনা ঘটতে পারে:
* Success: মেমোরিতে মান 5-ই ছিল। CAS সফলভাবে মান পরিবর্তন করে 6 করে দিল। কাজ শেষ এবং loop থেকে বেরিয়ে আসা হলো।

* Conflict: এই প্রক্রিয়ার মাঝখানে অন্য কোনো user মেমোরির মানটি পরিবর্তন করে 7 করে দিয়েছে। ফলে CAS যখন Check করল, তখন দেখল বর্তমান 
মান 5 নেই। CAS-এর অপারেশনটি সাথে সাথে Fail হলো।

* Retry: Fail হওয়ার পর লুপটি আবার প্রথম ধাপে ফিরে যাবে। এবার নতুন মান হিসেবে পড়া হবে 7। নতুন হিসাব হবে 8। এরপর আবার CAS command 
পাঠানো হবে: "যদি মান 7 থাকে, তবে 8 করো।" যতক্ষণ না পর্যন্ত CAS সফল হচ্ছে, ততক্ষণ এই প্রক্রিয়া চলতে থাকবে।
"""

"""
সাধারণ Python Varianable গুলো Hardware লেভেলের CAS Support করে না। তাই atomicx library install করে নিতে হবে

-> install command : pip install atomicx
"""

import time
import threading
from atomicx import AtomicInt

# Create an atomic integer with an initial value of 0
counter = AtomicInt()

def increment():

    # create a retry loop
    while True:
        old_value = counter.load()
        new_value = old_value + 1

        print("Current thread : ", threading.current_thread().name, ", Couter Value : ", old_value, ", New Value : ", new_value)
        # print("counter value : ", counter.load())
        # print("new value : ", new_value)

        # success, current_val = counter.compare_exchange(old_value, new_value)

        time.sleep(1)

        # correct CAS usage
        if counter.compare_exchange(old_value, new_value)[0]:
            print(f"{threading.current_thread().name}: {old_value} → {new_value}")
            break
        else:
            print(f"{threading.current_thread().name}: CAS failed, retrying...")


thread_list = []
num_threads = 10

for i in range(num_threads):
    t = threading.Thread(target=increment)
    thread_list.append(t)
    t.start()


for t in thread_list:
    t.join()

print("Final Counter Value : ", counter.load())

"""
-> compare_exchange(old_value, new_value) Method
compare_exchange() মেথডটি Atomic Operation Execute করে। এটি একটি Tuple Return করে।
Return Type: (Boolean, Current Actual Value)

1. Boolean (Success/Failure Flag)
এই Boolean মানটি নির্দেশ করে যে compare_exchange অপারেশনটি সফল হয়েছে কি না। 
* যদি True হয়: মেমোরিতে থাকা বর্তমান মানটি old_value-এর সাথে হুবহু মিলে গিয়েছে। ফলে সিস্টেম সফলভাবে সেই মানটিকে new_value দিয়ে প্রতিস্থাপন 
(Swap) করেছে। এটি একটি সফল অপারেশন নির্দেশ করে।
* যদি False হয়: old_value read করার পর এবং Update করার মাঝখানের সময়ে অন্য কোনো Thread মানটি update করে ফেলেছে। তাই কোনো update হয়নি।

২. Current Actual Value
এই value-টি অত্যন্ত গুরুত্বপূর্ণ। এটি নির্দেশ করে যে compare_exchange অপারেশনটি execute করার সময় মেমোরিতে আসলে কোন value-টি ছিল।
যদি Operation Fail করে, তাহলে এই value ব্যবহার করে পরবর্তী retry-এ সঠিক old_value হিসেবে ব্যবহার করা যায়।
"""
