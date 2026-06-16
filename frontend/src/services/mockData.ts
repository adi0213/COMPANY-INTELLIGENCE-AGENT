import type { CompanyResult } from '../store/companyStore';

/**
 * Curated mock intelligence data for popular companies.
 * Used as fallback when the FastAPI backend is unavailable.
 */
const MOCK_DATA: Record<string, CompanyResult> = {
  google: {
    company: 'Google',
    overview: `Google LLC is an American multinational technology corporation founded in 1998 by Larry Page and Sergey Brin. Headquartered in Mountain View, California, it is a subsidiary of Alphabet Inc.

• Industry: Technology, Internet, Cloud Computing, Artificial Intelligence
• Headquarters: Mountain View, California, USA
• CEO: Sundar Pichai
• Employees: ~180,000+
• Website: google.com
• Founded: September 4, 1998
• Revenue: $307 billion (2023)`,

    latest_developments: `• Gemini 2.0 Launch — Google released its most advanced multimodal AI model, competing directly with GPT-4 and Claude. (2024)
• NotebookLM Expansion — AI-powered research assistant expanded globally with audio overview features.
• Google Cloud AI — Vertex AI platform saw 300% growth in enterprise adoption.
• Waymo Robotaxi — Expanded autonomous ride-hailing to San Francisco, Phoenix, and Los Angeles.
• Android 15 — Released with on-device AI features and enhanced privacy controls.
• DeepMind AlphaFold 3 — Predicted structures of all known proteins, advancing drug discovery.`,

    key_technologies: `• Gemini — Next-generation multimodal AI model family (Nano, Pro, Ultra)
• TensorFlow & JAX — Open-source ML frameworks powering internal and external AI
• TPU v5p — Custom tensor processing units for large-scale AI training
• Kubernetes — Container orchestration (originally developed at Google)
• Vertex AI — Managed ML platform on Google Cloud
• BigQuery — Serverless data warehouse for analytics
• Spanner — Globally distributed relational database
• Flutter — Cross-platform mobile app framework
• Go (Golang) — Systems programming language developed at Google
• Angular — Frontend web application framework`,

    business_areas: `• Search & Advertising — Core revenue driver ($175B+), world's dominant search engine
• Google Cloud Platform (GCP) — Enterprise cloud services, 3rd largest cloud provider ($33B revenue)
• YouTube — Video streaming platform with 2.7B monthly users, growing ads + subscriptions
• Artificial Intelligence — Gemini, DeepMind, AI-powered products across the entire portfolio
• Android & Pixel — Mobile OS (3B+ devices) and hardware ecosystem
• Waymo — Autonomous vehicles and robotaxi services
• Google Workspace — Productivity suite (Gmail, Docs, Drive) with 3B+ users`,

    interview_focus: `Technical Interview Topics:
• Data Structures & Algorithms — Arrays, trees, graphs, dynamic programming (LeetCode Medium-Hard)
• System Design — Design Google Search, YouTube recommendations, Google Maps routing
• Machine Learning — Model training pipelines, feature engineering, A/B testing at scale
• Distributed Systems — MapReduce, consensus algorithms, eventual consistency
• Coding — Python, Java, C++, Go. Clean code, edge cases, time/space complexity

Behavioral Interview Topics:
• Googleyness & Leadership — Collaboration, humility, comfort with ambiguity
• Problem Solving — How you approach novel, open-ended challenges
• Project Impact — Quantifiable results from past work

Preparation Tips:
• Practice on LeetCode (aim for 200+ problems, focus on Medium difficulty)
• Study the Google SRE Book for infrastructure roles
• Prepare 5-6 STAR-format stories covering leadership and conflict resolution
• Expect 5-6 interview rounds (phone screen → onsite coding × 2 → system design → behavioral → hiring committee)`,

    hiring_trends: `Top Hiring Roles:
• Senior Software Engineer (L5/L6) — Largest hiring volume
• Machine Learning Engineer — Gemini, Cloud AI, DeepMind teams
• Site Reliability Engineer (SRE) — Critical infrastructure teams
• Product Manager — AI-first product strategy
• Research Scientist — DeepMind, Google Brain, Gemini

Departments with Most Openings:
• Google Cloud — Fastest growing division
• AI/ML — Gemini and foundational models
• YouTube — Creator tools and recommendation systems

Emerging Skill Requirements:
• LLM fine-tuning and prompt engineering
• Multimodal AI (vision + language + audio)
• Responsible AI and safety evaluation
• Kubernetes and cloud-native architecture`,

    salary_insights: `• Software Engineer (L3): $130,000 - $180,000 base + $50K-$100K stock
• Software Engineer (L4): $155,000 - $210,000 base + $80K-$150K stock
• Senior SWE (L5): $185,000 - $280,000 base + $150K-$300K stock
• Staff SWE (L6): $250,000 - $350,000 base + $250K-$500K stock
• ML Engineer (L4): $160,000 - $220,000 base + $100K-$200K stock
• Data Scientist (L4): $150,000 - $210,000 base + $80K-$160K stock
• Product Manager (L5): $180,000 - $270,000 base + $120K-$250K stock

Note: Total compensation includes base salary, annual bonus (15-20%), and RSU vesting over 4 years. Bay Area cost of living adjustments apply.`,

    executive_summary: `Google is aggressively expanding its AI strategy through the Gemini model family, custom TPU hardware, and Vertex AI cloud services, positioning itself as the leading full-stack AI company. While maintaining dominance in search and advertising ($175B+), Google Cloud is rapidly closing the gap with AWS and Azure, and Waymo is pioneering the autonomous vehicle market. The company faces regulatory headwinds from antitrust scrutiny but continues to attract top engineering talent with industry-leading compensation.`,
  },
};

// Generate reasonable mock data for any company not in our curated list
function generateGenericMock(companyName: string): CompanyResult {
  const name = companyName.charAt(0).toUpperCase() + companyName.slice(1);
  return {
    company: name,
    overview: `${name} is a prominent company operating in the technology and business sector. This analysis was generated using mock data because the backend AI pipeline is not currently running.\n\n• Industry: Technology\n• To see real AI-generated intelligence, start the FastAPI backend with: uvicorn app.main:app --reload`,
    latest_developments: `• ${name} continues to expand its product portfolio and market presence.\n• The company has been investing in AI and digital transformation initiatives.\n• Recent partnerships and acquisitions are strengthening its competitive position.`,
    key_technologies: `• Cloud Infrastructure — Modern cloud-native architecture\n• AI/ML — Machine learning integration across products\n• Data Analytics — Big data processing and business intelligence\n• Mobile — Cross-platform mobile applications`,
    business_areas: `• Core Products — Primary revenue-generating product lines\n• Cloud Services — Growing enterprise cloud division\n• AI & Innovation — Research and development in emerging technologies\n• International Expansion — Growing presence in global markets`,
    interview_focus: `Technical Topics:\n• Data Structures & Algorithms\n• System Design\n• Domain-specific technical knowledge\n\nBehavioral Topics:\n• Leadership and teamwork\n• Problem-solving approach\n• Communication skills\n\nTip: Research ${name}'s engineering blog and recent tech talks for company-specific preparation.`,
    hiring_trends: `• Software Engineering — Consistent demand across all levels\n• Data Science — Growing need for analytics and ML talent\n• Product Management — Strategic product leadership roles\n• Cloud/DevOps — Infrastructure and platform engineering`,
    salary_insights: `• Software Engineer: $120,000 - $200,000 base\n• Senior Engineer: $160,000 - $280,000 base\n• Data Scientist: $130,000 - $220,000 base\n• Product Manager: $140,000 - $250,000 base\n\nNote: Ranges are estimates. Actual compensation varies by location, level, and equity.`,
    executive_summary: `${name} is positioned in a competitive market landscape with opportunities for growth in AI, cloud computing, and digital services. The company's strategic investments in technology and talent acquisition suggest a forward-looking approach to market challenges. (This is demo data — connect the FastAPI backend for real AI-generated analysis.)`,
  };
}

// Pre-generate mocks for popular companies with customized data
const POPULAR_MOCKS: Record<string, Partial<CompanyResult>> = {
  microsoft: { company: 'Microsoft', executive_summary: 'Microsoft has transformed into a cloud-first, AI-first company under Satya Nadella, with Azure growing 29% YoY and a strategic partnership with OpenAI positioning it at the forefront of enterprise AI adoption. GitHub Copilot and Microsoft 365 Copilot are driving AI monetization across developer and productivity segments.' },
  amazon: { company: 'Amazon', executive_summary: 'Amazon dominates e-commerce and cloud computing through AWS ($90B+ revenue), while expanding into healthcare (One Medical), satellite internet (Kuiper), and AI services (Bedrock). The company continues to optimize logistics with robotics and AI-driven supply chain management.' },
  apple: { company: 'Apple', executive_summary: 'Apple is integrating AI across its ecosystem with Apple Intelligence, while maintaining premium hardware margins through iPhone, Mac (M-series chips), and a growing Services division ($85B+ revenue). The Vision Pro marks its entry into spatial computing.' },
  netflix: { company: 'Netflix', executive_summary: 'Netflix leads global streaming with 260M+ subscribers, leveraging sophisticated recommendation AI and an ad-supported tier for growth. The company is expanding into live sports, gaming, and interactive content while optimizing content spend through data-driven production decisions.' },
  openai: { company: 'OpenAI', executive_summary: 'OpenAI pioneered the generative AI revolution with ChatGPT and the GPT model family, achieving $3.4B+ ARR. The company is expanding into enterprise (ChatGPT Enterprise), developer tools (API platform), and multimodal AI while navigating governance challenges and intense competition.' },
  nvidia: { company: 'NVIDIA', executive_summary: 'NVIDIA has become the most valuable semiconductor company by dominating AI training and inference hardware with its GPU architecture (H100/B200). Data center revenue grew 400%+ as every major tech company and government races to build AI infrastructure. The CUDA ecosystem creates deep competitive moats.' },
  tesla: { company: 'Tesla', executive_summary: 'Tesla leads the global EV market while expanding into energy storage (Megapack), solar, and autonomous driving (FSD). The company is developing Optimus humanoid robots and maintains manufacturing advantages through vertical integration and gigafactory scale.' },
  meta: { company: 'Meta', executive_summary: 'Meta is making massive AI investments with the open-source Llama model family while maintaining social media dominance through Facebook, Instagram, WhatsApp (3.9B+ total users). Reality Labs continues metaverse development despite losses, while Reels competes effectively with TikTok.' },
  spotify: { company: 'Spotify', executive_summary: 'Spotify leads music streaming with 640M+ users and is expanding into podcasts, audiobooks, and AI-powered personalization. The company achieved sustained profitability through margin optimization and premium subscriber growth while leveraging AI for content discovery and creator tools.' },
};

export function getMockCompanyData(companyName: string): CompanyResult {
  const key = companyName.toLowerCase().trim();

  // Check curated detailed mocks first
  if (MOCK_DATA[key]) return MOCK_DATA[key];

  // Check if we have a partial mock with a customized summary
  const partial = POPULAR_MOCKS[key];
  if (partial) {
    const generic = generateGenericMock(companyName);
    return { ...generic, ...partial };
  }

  // Generate a generic mock for unknown companies
  return generateGenericMock(companyName);
}
