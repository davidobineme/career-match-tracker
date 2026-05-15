import json

import re
# re is used for "regular expressions"

from datetime import date

JOB_FILES = "jobs.json"
COMMON_WORDS = {"the", "and", "for", "with", "you", "your", "are", "this", "that",
               "will", "have", "from", "our", "has", "job", "role", "team", "work",
               "can", "all", "but", "not", "was", "were", "they", "their", "about",
               "into", "over", "such", "more", "than", "also", "who", "what"}


def load_jobs():
    try:
        with open(JOB_FILES, "r") as file:
            return json.load(file)
    
    except FileNotFoundError:
        return[]
    # Try is used to open the jobs.json in read mode. Json.load turns the data into python data.
    # We return an empty list if the jobs.json dont exist instead of crashing

def save_jobs(jobs):
    with open(JOB_FILES, "w") as file:
        json.dump(jobs, file, indent=4)

    # "w" means write mode and create the files if they don't already exist. If it already does then it just updates the list
    # indent=4 makes it easier to read

def clean_text(text):
    text = text.lower()
    words = re.findall(r"\b[a-zA-Z]+\b", text)
    # re.findall finds all words made of letters and removes punctuations.
    cleaned_words = []
    for word in words:
        if word not in COMMON_WORDS and len(word) > 2:
            cleaned_words.append(word)

    return cleaned_words

def analyze_resume(job_description, resume_text):
    job_words = clean_text(job_description)
    resume_words = clean_text(resume_text)

    job_words = set(job_words)
    resume_words = set(resume_words)
    # set() removes duplicates

    matched_words = job_words.intersection(resume_words)
    missing_words = job_words.difference(resume_words)
    # INTERSECTION finds words in both the description and resume
    # DIFFERENCE finds words in the description but not in the resume

    if len(job_words) == 0:
        match_score = 0
    else:
        match_score = round((len(matched_words) / len(job_words)) * 100, 2)

    return {
        "match_score": match_score,
        "matched_keywords": sorted(list(matched_words)),
        "missing_keywords": sorted(list(missing_words))
    }

def get_multiline_input(prompt):
    print(prompt)
    print("Paste your text below. Type DONE on a new line when finished.")

    # Multiline input was used because of how long the texts inputed my stretch out to be

    lines = []

    while True:
        line = input()

        if line == "DONE":
            break

        lines.append(line)

    return "\n".join(lines)

def add_job():
    print("\nAdd a New Job")

    company = input("Company name: ")
    title = input("Job title: ")
   
    description = get_multiline_input("\nPaste the job description below:\n")
    resume = get_multiline_input("\nPaste your resume text below:\n")

    analysis = analyze_resume(description, resume)

    job = {# Creates a job record; This is a dictionary.
        "company": company,
        "title": title,
        "date_added": str(date.today()),
        "status": "Interested",
        "match_score": analysis["match_score"],
        "matched_keywords": analysis["matched_keywords"],
        "missing_keywords": analysis["missing_keywords"][:20]
        # [:20] means only save the first 20 missing keywords.
        # This keeps the saved file from becoming huge.

    }
    jobs = load_jobs() # Loads old jobs 
    
    jobs.append(job) # Add the new jobs 

    save_jobs(jobs) # Saves the updated list
    
    print("\nJob saved!")
    print(f"Match Score: {analysis['match_score']}%")
    print("\nTop Missing Keywords:")
    
    for keyword in analysis["missing_keywords"][:10]:
        print("-", keyword)


def view_jobs():

    print("\nSaved Jobs")

    jobs = load_jobs()

    if len(jobs) == 0:
        print("No jobs saved yet.")

        return

    for index, job in enumerate(jobs, start=1):

        print("\n-----------------------------")

        print(f"{index}. {job['title']} at {job['company']}")
        print(f"Date Added: {job['date_added']}")
        print(f"Status: {job['status']}")
        print(f"Match Score: {job['match_score']}%")
        print("Missing Keywords:")
        
        for keyword in job["missing_keywords"][:5]:
            print("-", keyword)



def update_job_status():
    print("\nUpdate Job Status")

    jobs = load_jobs()

    if len(jobs) == 0:
        print("No jobs saved yet.")
        return

    for index, job in enumerate(jobs, start=1):
        print(f"\n{index}. {job['title']} at {job['company']}")
        print(f"Current Status: {job['status']}")

    choice = input("\nChoose the job number you want to update: ")

    if choice.isdigit() == False:
        print("Please enter a valid number.")
        return

    job_index = int(choice) - 1

    if job_index < 0 or job_index >= len(jobs):
        print("That job number does not exist.")
        return

    print("\nStatus Options:")
    print("1. Interested")
    print("2. Applied")
    print("3. Interview")
    print("4. Offer")
    print("5. Rejected")
    print("6. Ghosted\n")
    status_choice = input("Choose a new status: ")

    if status_choice == "1":
        new_status = "Interested"
    elif status_choice == "2":
        new_status = "Applied"
    elif status_choice == "3":
        new_status = "Interview"
    elif status_choice == "4":
        new_status = "Offer"
    elif status_choice == "5":
        new_status = "Rejected"
    elif status_choice == "6":
        new_status = "Ghosted"
    else:
        print("Invalid status choice.")
        return

    jobs[job_index]["status"] = new_status

    save_jobs(jobs)
    print("\nJob status updated!")

def delete_job():
    print("\nDelete Saved Job")

    jobs = load_jobs()

    if len(jobs) == 0:
        print("No jobs saved yet.")
        return
    
    for index, job in enumerate(jobs, start=1):
        print(f"\n{index}. {job['title']} at {job['company']}")
        print(f"Status: {job['status']}")

    choice = input("\nChoose the job number you want to delete: ")

    if choice.isdigit() == False:
        print("Please enter a valid number.")
        return
    
    job_index = int(choice) - 1

    if job_index < 0 or job_index >= len(jobs):
        print("That job number does not exist.")
        return
    
    print(f"\nYou are about to delete: {jobs[job_index]['title']} at {jobs[job_index]['company']}")
    confirm = input("Are you sure? Type yes to delete: ")

    if confirm.lower() == "yes":
        deleted_job = jobs.pop(job_index)
        save_jobs(jobs)

        print(f"\nDeleted {deleted_job['title']} at {jobs[job_index]['company']}")
    else:
        print("\nDelete canceled")

def main():
    while True:

        print("\nCareerMatch Tracker\n")
        print("1. Add job and analyze resume")
        print("2. View saved jobs")
        print("3. Update job status")
        print("4. Delete saved job")
        print("5. Exit\n")

        choice = input("Choose an option: ")
        
        if choice == "1":
            add_job()
        elif choice == "2":
            view_jobs()
        elif choice == "3":
            update_job_status()
        elif choice == "4":
            delete_job()
        elif choice == "5":
            print("Goodbye!")
            break
        else:
            print("Invalid option. Please choose 1, 2, 3, 4, or 5.") 
        

if __name__ == "__main__":
    main( )