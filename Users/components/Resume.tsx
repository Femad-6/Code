import React from 'react';
import { RESUME_DATA } from '../constants';
import { Icons } from './Icons';
import { ContactInfo, Education, Project, SkillCategory, Award } from '../types';

// Helper Components
const SectionTitle = ({ icon: Icon, title }: { icon: any, title: string }) => (
  <div className="flex items-center gap-2 mb-4 border-b-2 border-slate-200 pb-2 text-slate-800">
    <div className="p-1.5 bg-accent/10 rounded-md text-accent">
      <Icon size={18} />
    </div>
    <h2 className="text-lg font-bold uppercase tracking-wide">{title}</h2>
  </div>
);

interface TagProps {
  children: React.ReactNode;
  primary?: boolean;
}

const Tag: React.FC<TagProps> = ({ children, primary = false }) => (
  <span className={`inline-flex items-center px-2 py-0.5 rounded text-xs font-medium mr-2 mb-1 ${
    primary 
      ? 'bg-accent text-white' 
      : 'bg-slate-100 text-slate-700 border border-slate-200'
  }`}>
    {children}
  </span>
);

export const Resume: React.FC = () => {
  const { name, title, contact, education, skills, projects, awards, summary, interests, englishLevel } = RESUME_DATA;

  const handlePrint = () => {
    window.print();
  };

  return (
    <div className="min-h-screen p-4 md:p-8 flex justify-center items-start text-slate-700">
      {/* Floating Print Button */}
      <button 
        onClick={handlePrint}
        className="no-print fixed bottom-8 right-8 bg-accent hover:bg-blue-700 text-white p-4 rounded-full shadow-lg transition-all hover:scale-105 z-50 flex items-center gap-2 font-semibold"
        title="Print or Save as PDF"
      >
        <Icons.Download size={20} />
        <span className="hidden md:inline">保存 PDF</span>
      </button>

      {/* A4 Paper Container */}
      <div className="w-full max-w-[210mm] bg-white shadow-xl print-shadow-none md:min-h-[297mm] overflow-hidden rounded-sm relative">
        
        {/* Header Section */}
        <header className="bg-slate-900 text-white p-8 md:p-10">
          <div className="flex flex-col md:flex-row justify-between items-start md:items-end gap-6">
            <div className="space-y-2">
              <h1 className="text-4xl md:text-5xl font-bold tracking-tight">{name}</h1>
              <p className="text-xl md:text-2xl text-slate-300 font-light">{title}</p>
            </div>
            
            <div className="flex flex-col gap-2 text-sm md:text-base text-slate-300">
              <div className="flex items-center gap-2">
                <Icons.Phone size={16} className="text-accent" />
                <span>{contact.phone}</span>
              </div>
              <div className="flex items-center gap-2">
                <Icons.Mail size={16} className="text-accent" />
                <a href={`mailto:${contact.email}`} className="hover:text-white transition-colors">{contact.email}</a>
              </div>
              {contact.location && (
                <div className="flex items-center gap-2">
                  <Icons.MapPin size={16} className="text-accent" />
                  <span>{contact.location}</span>
                </div>
              )}
            </div>
          </div>
        </header>

        {/* Main Content Grid */}
        <div className="grid grid-cols-1 md:grid-cols-12 gap-0">
          
          {/* Left Column (Sidebar Style) - 4 Cols */}
          <aside className="md:col-span-4 bg-slate-50 p-8 border-r border-slate-100 space-y-8">
            
            {/* Education */}
            <section>
              <SectionTitle icon={Icons.Education} title="教育背景" />
              <div className="space-y-4">
                <div>
                  <h3 className="font-bold text-slate-900">{education.school}</h3>
                  <div className="flex flex-wrap gap-1 mt-1 mb-2">
                    {education.tags.map(tag => (
                      <Tag key={tag} primary>{tag}</Tag>
                    ))}
                  </div>
                  <p className="text-sm font-medium">{education.major} | {education.degree}</p>
                  <p className="text-xs text-slate-500 mb-2">{education.year}</p>
                  <ul className="text-sm space-y-1.5 list-disc list-outside ml-4 text-slate-600">
                    {education.details.map((detail, idx) => (
                      <li key={idx} dangerouslySetInnerHTML={{ 
                        __html: detail.replace(/前 7%|13\/182/g, '<b>$&</b>') 
                      }} />
                    ))}
                  </ul>
                </div>
              </div>
            </section>

            {/* Skills */}
            <section>
              <SectionTitle icon={Icons.Chip} title="专业技能" />
              <div className="space-y-4">
                {skills.map((skillGroup, idx) => (
                  <div key={idx}>
                    <h4 className="text-sm font-bold text-slate-800 mb-2 border-l-2 border-accent pl-2">
                      {skillGroup.category}
                    </h4>
                    <div className="flex flex-wrap gap-1.5">
                      {skillGroup.items.map(item => (
                        <span key={item} className="text-xs bg-white border border-slate-200 px-2 py-1 rounded text-slate-700">
                          {item}
                        </span>
                      ))}
                    </div>
                  </div>
                ))}
              </div>
            </section>

             {/* Interests / Hobbies */}
             {interests && interests.length > 0 && (
              <section>
                <SectionTitle icon={Icons.Heart} title="爱好与特长" />
                <ul className="text-sm space-y-2 text-slate-600">
                  {interests.map((interest, idx) => (
                     <li key={idx} className="flex items-start gap-2">
                        <span className="text-accent mt-0.5 min-w-[4px]">▪</span>
                        <span>{interest}</span>
                     </li>
                  ))}
                </ul>
              </section>
            )}

            {/* Language */}
            {englishLevel && (
              <section>
                <SectionTitle icon={Icons.Languages} title="英语水平" />
                <div className="font-medium text-slate-700 flex items-center gap-2">
                  <span className="w-1.5 h-1.5 bg-accent rounded-full"></span>
                  {englishLevel}
                </div>
              </section>
            )}

          </aside>

          {/* Right Column (Main Content) - 8 Cols */}
          <main className="md:col-span-8 p-8 space-y-8">

            {/* Self Evaluation / Summary */}
            <section className="print-break-inside-avoid">
              <SectionTitle icon={Icons.User} title="自我评价" />
              <p className="text-sm leading-relaxed text-slate-600 text-justify">
                {summary}
              </p>
            </section>

            {/* Project Experience */}
            <section>
              <SectionTitle icon={Icons.Code} title="项目经历" />
              <div className="space-y-6">
                {projects.map((project, idx) => (
                  <div key={idx} className="print-break-inside-avoid">
                    <div className="flex flex-col sm:flex-row sm:justify-between sm:items-baseline mb-2">
                      <h3 className="text-lg font-bold text-slate-900">{project.name}</h3>
                      <span className="text-sm font-medium text-accent bg-blue-50 px-2 py-0.5 rounded">
                        {project.role}
                      </span>
                    </div>
                    
                    <p className="text-sm text-slate-600 mb-3 italic">
                      {project.description}
                    </p>

                    <div className="mb-3">
                      {project.techStack.map(tech => (
                        <Tag key={tech}>{tech}</Tag>
                      ))}
                    </div>

                    <ul className="text-sm space-y-2 list-none">
                      {project.achievements.map((achievement, aIdx) => (
                        <li key={aIdx} className="relative pl-5 before:content-['▹'] before:absolute before:left-0 before:text-accent">
                          {achievement}
                        </li>
                      ))}
                    </ul>
                  </div>
                ))}
              </div>
            </section>

            {/* Awards */}
            <section>
              <SectionTitle icon={Icons.Award} title="奖项与证书" />
              <div className="grid grid-cols-1 gap-4">
                {awards.map((award, idx) => (
                  <div key={idx} className="flex items-start gap-3 p-3 bg-slate-50 rounded-lg border border-slate-100 print-break-inside-avoid">
                    <div className="mt-1 text-yellow-500">
                      <Icons.Award size={20} fill="currentColor" className="opacity-80" />
                    </div>
                    <div>
                      <h4 className="font-bold text-slate-900">{award.rank}</h4>
                      <p className="text-sm font-medium text-slate-700">{award.title}</p>
                      {award.description && (
                        <p className="text-xs text-slate-500 mt-0.5">{award.description}</p>
                      )}
                    </div>
                  </div>
                ))}
              </div>
            </section>

          </main>
        </div>
      </div>
    </div>
  );
};