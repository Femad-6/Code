export interface ContactInfo {
  phone: string;
  email: string;
  github?: string;
  location?: string;
}

export interface Education {
  school: string;
  degree: string;
  major: string;
  year: string;
  tags: string[]; // e.g. "211", "Double First Class"
  details: string[]; // GPA, Courses, etc.
}

export interface SkillCategory {
  category: string;
  items: string[];
}

export interface Project {
  name: string;
  role: string;
  description: string;
  techStack: string[];
  achievements: string[];
}

export interface Award {
  title: string;
  rank: string;
  description?: string;
}

export interface ResumeData {
  name: string;
  title: string;
  contact: ContactInfo;
  summary: string;
  education: Education;
  skills: SkillCategory[];
  projects: Project[];
  awards: Award[];
  interests: string[];
  englishLevel?: string;
}