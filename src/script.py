import os
import logging
import datetime
from typing import List, Optional
from email.mime.text import MIMEText
from dotenv import load_dotenv
import smtplib
import requests
from requests.exceptions import RequestException

load_dotenv()

logging.basicConfig(
    filename='linkedin-post-generator.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class Config:
    TECH_LIST: List[str] = ["React.js", "Node.js", "TypeScript", "AWS", "PostgreSQL", "Docker"]
    SENDER_EMAIL: str = os.getenv("SENDER_EMAIL", "")
    RECEIVER_EMAIL: str = os.getenv("RECEIVER_EMAIL", "")
    EMAIL_PASSWORD: str = os.getenv("EMAIL_PASSWORD", "")
    SMTP_SERVER: str = os.getenv("SMTP_SERVER", "smtp.gmail.com")
    SMTP_PORT: int = int(os.getenv("SMTP_PORT", 465))
    OLLAMA_API_URL: str = os.getenv("OLLAMA_API_URL", "http://localhost:11434/api/generate")
    OLLAMA_MODEL: str = os.getenv("OLLAMA_MODEL", "llama3")

def get_tech_of_the_day(tech_list: List[str]) -> str:
    if not tech_list:
        logger.error("Technology list is empty")
        raise ValueError("Technology list cannot be empty")
    current_day = datetime.datetime.now().day
    return tech_list[current_day % len(tech_list)]

def generate_post_prompt(tech: str) -> str:
    return (
        f"You are a full-stack web developer with expertise in modern technologies such as React.js, Node.js, "
        f"TypeScript, React Native, and databases like MySQL, PostgreSQL, and MariaDB. You have professional "
        f"experience building web solutions, including APIs and front-end features, and have worked with tools "
        f"like Git, Docker, and AWS. Your projects include a web-based evaluation system and a tourist guide app, "
        f"showcasing your skills in scalable and user-friendly development. Write LinkedIn posts (150-300 words) "
        f"in a professional and serious tone, in English, focusing on explaining what {tech} is and why it is "
        f"valuable in development. Avoid personal anecdotes or detailed tutorials with code—emphasize its purpose "
        f"and benefits. After writing in English, provide a translation to Portuguese with the same tone."
    )

def generate_post(tech: str, api_url: str, model: str) -> str:
    try:
        prompt = generate_post_prompt(tech)
        response = requests.post(
            api_url,
            json={"model": model, "prompt": prompt},
            timeout=30
        )
        response.raise_for_status()
        post_content = response.json().get("response", "")
        if not post_content:
            raise ValueError("Empty response from API")
        logger.info(f"Post generated successfully for {tech}")
        return post_content
    except RequestException as e:
        logger.error(f"Failed to generate post for {tech}: {str(e)}")
        raise RuntimeError(f"API request failed: {str(e)}") from e

def send_email(post: str, tech: str, config: Config) -> None:
    try:
        msg = MIMEText(post)
        msg['Subject'] = f'Daily LinkedIn Post - {tech}'
        msg['From'] = config.SENDER_EMAIL
        msg['To'] = config.RECEIVER_EMAIL

        with smtplib.SMTP_SSL(config.SMTP_SERVER, config.SMTP_PORT) as server:
            server.login(config.SENDER_EMAIL, config.EMAIL_PASSWORD)
            server.sendmail(config.SENDER_EMAIL, config.RECEIVER_EMAIL, msg.as_string())
        logger.info(f"Email sent successfully for {tech}")
    except smtplib.SMTPException as e:
        logger.error(f"Failed to send email for {tech}: {str(e)}")
        raise RuntimeError(f"Email sending failed: {str(e)}") from e

def main() -> None:
    config = Config()

    if not all([config.SENDER_EMAIL, config.RECEIVER_EMAIL, config.EMAIL_PASSWORD]):
        logger.error("Missing email configuration")
        raise ValueError("Email configuration is incomplete")

    try:
        tech = get_tech_of_the_day(config.TECH_LIST)
        logger.info(f"Generating post for technology: {tech}")
        
        post = generate_post(tech, config.OLLAMA_API_URL, config.OLLAMA_MODEL)
        send_email(post, tech, config)
        
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        raise

if __name__ == "__main__":
    main()