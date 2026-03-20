#!/usr/bin/env python3
"""Random utility functions."""

import random


def get_random_number(min_val: int = 1, max_val: int = 100) -> int:
    """Generate a random integer between min_val and max_val.

    Args:
        min_val: Minimum value (inclusive).
        max_val: Maximum value (inclusive).

    Returns:
        A random integer.
    """
    return random.randint(min_val, max_val)


def get_random_joke() -> str:
    """Return a random joke.

    Returns:
        A string containing a random joke.
    """
    jokes = [
        "Why don't scientists trust atoms? Because they make up everything!",
        "What do you call fake spaghetti? An impasta!",
        "Why did the scarecrow win an award? Because he was outstanding in his field!",
        "What do you get when you cross a snowman and a vampire? Frostbite!",
        "Why don't eggs tell jokes? They'd crack each other up!"
    ]
    return random.choice(jokes)


def random_color() -> str:
    """Return a random color name.

    Returns:
        A random color string.
    """
    colors = ["red", "blue", "green", "yellow", "purple", "orange", "pink", "black", "white"]
    return random.choice(colors)


def generate_random_user_profile(count: int = 1) -> list:
    """Generate random user profiles with personal and contact information.
    
    This function creates realistic-looking user profiles with names, emails,
    phone numbers, addresses, and other personal details for testing purposes.
    
    Args:
        count: Number of user profiles to generate (default: 1).
    
    Returns:
        A list of dictionaries containing user profile information.
    """
    first_names = ["Rajesh", "Priya", "Amit", "Sneha", "Vikram", "Anjali", "Rohit", "Divya", "Nikhil", "Kanika"]
    last_names = ["Sharma", "Verma", "Singh", "Gupta", "Patel", "Iyer", "Nair", "Bhat", "Khanna", "Rao"]
    domains = ["gmail.com", "yahoo.com", "outlook.com", "company.com", "email.co.in"]
    cities = ["Delhi", "Mumbai", "Bangalore", "Pune", "Hyderabad", "Ahmedabad", "Chennai", "Kolkata", "Jaipur", "Lucknow"]
    job_titles = ["Software Engineer", "Data Analyst", "Product Manager", "Designer", "DevOps Engineer", 
                  "Business Analyst", "QA Engineer", "Consultant", "Manager", "Director"]
    companies = ["TechCorp", "DataSoft", "CloudVision", "InnovateLabs", "FutureTech", "DigitalWorks", "SmartSystems", "CodeFlow"]
    
    profiles = []
    
    for _ in range(count):
        first_name = random.choice(first_names)
        last_name = random.choice(last_names)
        email = f"{first_name.lower()}.{last_name.lower()}@{random.choice(domains)}"
        phone = f"+91-{random.randint(9000000000, 9999999999)}"
        
        profile = {
            "id": random.randint(1000, 999999),
            "first_name": first_name,
            "last_name": last_name,
            "full_name": f"{first_name} {last_name}",
            "email": email,
            "phone": phone,
            "age": random.randint(22, 65),
            "city": random.choice(cities),
            "country": "India",
            "job_title": random.choice(job_titles),
            "company": random.choice(companies),
            "salary": random.randint(300000, 2000000),
            "experience_years": random.randint(1, 20),
            "is_active": random.choice([True, False]),
            "join_date": f"2020-{random.randint(1, 12):02d}-{random.randint(1, 28):02d}",
            "last_login": f"2024-{random.randint(1, 12):02d}-{random.randint(1, 28):02d}",
            "skills": random.sample(["Python", "Java", "JavaScript", "SQL", "AWS", "Docker", "Kubernetes", "React", "Angular", "Node.js"], 
                                   k=random.randint(3, 6)),
            "certifications": random.sample(["AWS Certified", "Azure Certified", "GCP Certified", "Agile", "PMP", "CISSP"], 
                                          k=random.randint(1, 3))
        }
        profiles.append(profile)
    
    return profiles
