import os
import re
from collections import Counter
from difflib import SequenceMatcher

class ResumeMatcher:
    def __init__(self):
        self.stop_words = {
            'i', 'me', 'my', 'myself', 'we', 'our', 'ours', 'ourselves', 
            'you', 'your', 'yours', 'yourself', 'yourselves', 'he', 'him', 
            'his', 'himself', 'she', 'her', 'hers', 'herself', 'it', 'its', 
            'itself', 'they', 'them', 'their', 'theirs', 'themselves', 
            'what', 'which', 'who', 'whom', 'this', 'that', 'these', 'those', 
            'am', 'is', 'are', 'was', 'were', 'be', 'been', 'being', 'have', 
            'has', 'had', 'having', 'do', 'does', 'did', 'doing', 'a', 'an', 
            'the', 'and', 'but', 'if', 'or', 'because', 'as', 'until', 'while',
            'of', 'at', 'by', 'for', 'with', 'about', 'against', 'between',
            'into', 'through', 'during', 'before', 'after', 'above', 'below',
            'to', 'from', 'up', 'down', 'in', 'out', 'on', 'off', 'over',
            'under', 'again', 'further', 'then', 'once', 'here', 'there',
            'when', 'where', 'why', 'how', 'all', 'any', 'both', 'each',
            'few', 'more', 'most', 'other', 'some', 'such', 'no', 'nor',
            'not', 'only', 'own', 'same', 'so', 'than', 'too', 'very', 'can',
            'will', 'just', 'don', 'should', 'now'
        }

    def preprocess_text(self, text):
        """Clean and prepare text for analysis"""
        text = re.sub(r'[^\w\s]', '', text.lower())
        words = [word for word in text.split() 
                if word not in self.stop_words and len(word) > 3]
        return words

    def extract_keywords(self, text, top_n=15):
        """Extract most important keywords"""
        words = self.preprocess_text(text)
        word_counts = Counter(words)
        return [word for word, count in word_counts.most_common(top_n)]

    def calculate_similarity(self, text1, text2):
        """Calculate similarity between two texts"""
        words1 = self.preprocess_text(text1)
        words2 = self.preprocess_text(text2)
        
        # Jaccard similarity
        set1 = set(words1)
        set2 = set(words2)
        jaccard = len(set1 & set2) / len(set1 | set2) if (set1 | set2) else 0
        
        # Sequence similarity
        seq_similarity = SequenceMatcher(None, ' '.join(words1), ' '.join(words2)).ratio()
        
        # Combined score (0-100)
        return min(100, int(((jaccard * 0.6) + (seq_similarity * 0.4)) * 100))

    def analyze_match(self, resume_text, job_text):
        """Generate comprehensive analysis report"""
        if not resume_text or not job_text:
            return "Error: Empty resume or job description provided"
        
        score = self.calculate_similarity(resume_text, job_text)
        job_keywords = self.extract_keywords(job_text)
        resume_keywords = self.extract_keywords(resume_text)
        
        matching = set(job_keywords) & set(resume_keywords)
        missing = set(job_keywords) - set(resume_keywords)
        
        report = [
            "\nRESUME-JOB MATCH ANALYSIS",
            "-------------------------",
            f"Match Score: {score}/100",
            "",
            "TOP MATCHING KEYWORDS:",
            ", ".join(sorted(matching)) if matching else "No strong matches found",
            "",
            "IMPORTANT MISSING KEYWORDS:",
            ", ".join(sorted(missing)) if missing else "No critical keywords missing",
            "",
            "SUGGESTIONS:",
            f"1. Add these terms to your resume: {', '.join(sorted(missing)[:5])}" if missing else "1. Good keyword coverage",
            f"2. Highlight these skills: {', '.join(sorted(matching)[:5])}" if matching else "2. Add more relevant skills",
            "3. Use numbers/metrics to quantify achievements",
            "",
            "Note: This analysis is based on keyword matching. For best results:",
            "- Tailor your resume to each job application",
            "- Mirror the language used in the job description",
            "- Include specific examples of your accomplishments"
        ]
        
        return "\n".join(report)

def read_file(file_path):
    """Read file with explicit error handling"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read()
    except FileNotFoundError:
        print(f"Error: File not found - {file_path}")
        return None
    except Exception as e:
        print(f"Error reading {file_path}: {str(e)}")
        return None

def main():
    print("\nFREE RESUME ANALYZER")
    print("--------------------")
    
    # Initialize analyzer
    matcher = ResumeMatcher()
    
    # Get input files
    print("\nPlease make sure you have these files in the same folder:")
    print("- job.txt (contains the job description)")
    print("- resume.txt (contains your resume text)")
    
    job_file = "job.txt"
    resume_file = "resume.txt"
    
    # Verify files exist
    if not all(os.path.exists(f) for f in [job_file, resume_file]):
        print("\nERROR: Missing required files!")
        print(f"Current directory: {os.getcwd()}")
        print("Please create both job.txt and resume.txt in this folder")
        return
    
    # Read files
    print("\nReading files...")
    job_text = read_file(job_file)
    resume_text = read_file(resume_file)
    
    if not job_text:
        print(f"Failed to read {job_file}")
        return
    if not resume_text:
        print(f"Failed to read {resume_file}")
        return
    
    # Analyze and display results
    print("\nAnalyzing your resume against the job description...")
    analysis = matcher.analyze_match(resume_text, job_text)
    
    print("\n" + "="*50)
    print(analysis)
    print("="*50)
    
    # Save results
    with open("analysis_results.txt", "w", encoding="utf-8") as f:
        f.write(analysis)
    print("\nResults saved to 'analysis_results.txt'")

if __name__ == "__main__":
    main()
