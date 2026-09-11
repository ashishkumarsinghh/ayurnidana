/* eslint-disable @typescript-eslint/no-explicit-any */
"use client";

import { useState, useEffect } from "react";
import { ArrowRight, Leaf, Sparkles, Wind, Flame, Droplets, ArrowLeft, HeartPulse, Stethoscope, CheckCircle2, XCircle, Printer, Pill, GlassWater, Clock, BookOpen, Activity, History, UserCircle, LogOut, Moon, Utensils } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Textarea } from "@/components/ui/textarea";
import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";

type Step = "WELCOME" | "AUTH" | "HISTORY" | "INTAKE" | "COMPLAINT" | "SIGNALS" | "LOADING" | "RESULTS";

const TONGUE_OPTS = [
  { val: "clean", label: "Clean & Pink", sub: "Healthy & normal" },
  { val: "white", label: "White Coated", sub: "Thick or milky" },
  { val: "red", label: "Red / Inflamed", sub: "Sensitive or raw" },
  { val: "dry", label: "Dry & Cracked", sub: "Rough or mapped" },
];

const STOOL_OPTS = [
  { val: "normal", label: "Regular", sub: "Well-formed, easy" },
  { val: "hard", label: "Hard & Dry", sub: "Constipation, pebbles" },
  { val: "loose", label: "Loose", sub: "Watery or urgent" },
  { val: "sticky", label: "Sticky", sub: "Heavy, mucus, foul" },
];

const HUNGER_OPTS = [
  { val: "normal", label: "Normal", sub: "Steady appetite" },
  { val: "intense", label: "Intense", sub: "Sharp, urgent, hangs" },
  { val: "irregular", label: "Irregular", sub: "Fluctuates daily" },
  { val: "weak", label: "Weak", sub: "Sluggish or absent" },
];

export default function Home() {
  const [step, setStep] = useState<Step>("WELCOME");
  
  // Auth State
  const [user, setUser] = useState<any>(null);
  const [authMode, setAuthMode] = useState<"LOGIN" | "REGISTER">("LOGIN");
  const [authIdent, setAuthIdent] = useState("");
  const [authPass, setAuthPass] = useState("");
  const [authName, setAuthName] = useState("");
  
  // History State
  const [historyList, setHistoryList] = useState<any[]>([]);

  // Consult State
  const [patientAge, setPatientAge] = useState<string>("30");
  const [comorbidities, setComorbidities] = useState<string>("");
  const [story, setStory] = useState("");
  const [tongue, setTongue] = useState<string | null>(null);
  const [stool, setStool] = useState<string | null>(null);
  const [hunger, setHunger] = useState<string | null>(null);
  const [results, setResults] = useState<any>(null);

  // Chat State
  const [chatQ, setChatQ] = useState("");
  const [chatA, setChatA] = useState("");
  const [isChatLoading, setIsChatLoading] = useState(false);

  const handleAuth = async () => {
    try {
      const endpoint = authMode === "LOGIN" ? "/api/auth/login" : "/api/auth/register";
      const payload = authMode === "LOGIN" 
        ? { identity: authIdent, password: authPass }
        : { username: authIdent.split('@')[0], email: authIdent, password: authPass, full_name: authName, age: 35, gender: "Other" };
        
      const res = await fetch(`${process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000"}${endpoint}`, {
        method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify(payload)
      });
      const data = await res.json();
      if (!res.ok) throw new Error(data.detail || "Auth failed");
      setUser(data.user);
      setStep("WELCOME");
    } catch (err: any) {
      alert(err.message);
    }
  };

  const fetchHistory = async () => {
    if (!user) return;
    const res = await fetch(`${process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000"}/api/history/${user.id}`);
    const data = await res.json();
    setHistoryList(data);
    setStep("HISTORY");
  };

  const handleRunConsultation = async () => {
    setStep("LOADING");

    try {
      const extRes = await fetch(`${process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000"}/api/symptoms/extract`, {
        method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify({ story }),
      });
      const extData = await extRes.json();

      const consRes = await fetch(`${process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000"}/api/consult`, {
        method: "POST", headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ patient_name: user?.full_name || "Guest", age: parseInt(patientAge) || 35, gender: user?.gender || "Male", comorbidities: comorbidities, symptoms: extData.extracted || {}, tongue: tongue || "clean", stool: stool || "normal", hunger: hunger || "normal" }),
      });
      const consData = await consRes.json();
      setResults(consData);
      
      if (user) {
        await fetch(`${process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000"}/api/history`, {
          method: "POST", headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ 
            user_id: user.id, 
            story, 
            symptoms: extData.extracted || {}, 
            primary_condition: consData.diagnosis.primary_condition, 
            sanskrit_name: consData.diagnosis.sanskrit_name, 
            dosha_scores: consData.dosha_pct, 
            treatment_summary: "Generated online plan",
            case_sheet_md: JSON.stringify(consData)
          })
        });
      }

      setTimeout(() => setStep("RESULTS"), 1000);
    } catch {
      alert("Error connecting to backend API.");
      setStep("SIGNALS");
    }
  };

  const handleChat = async () => {
    if (!chatQ.trim()) return;
    setIsChatLoading(true);
    try {
      const res = await fetch(`${process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000"}/api/chat`, {
        method: "POST", headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ patient_summary: "Guest, 35 yrs", diagnosis_summary: `${results?.diagnosis?.primary_condition}`, treatment_summary: "Herbal formulations prescribed", user_question: chatQ }),
      });
      const data = await res.json();
      setChatA(data.reply);
    } catch {
      setChatA("AyurVaidya is currently unreachable.");
    }
    setIsChatLoading(false);
  };

  const downloadPDF = async () => {
    const { jsPDF } = await import("jspdf");
    const doc = new jsPDF({ unit: "mm", format: "a4", orientation: "portrait" });
    
    let y = 15;
    const margin = 15;
    const pageWidth = 180; // 210 - 30 margin

    const addWrappedText = (text: string, x: number, currentY: number, width: number) => {
      const lines = doc.splitTextToSize(text, width);
      doc.text(lines, x, currentY);
      return lines.length * 4.5;
    };

    const checkPageBreak = (neededHeight: number) => {
      if (y + neededHeight > 280) {
        doc.addPage();
        y = 15;
      }
    };

    const addSectionHeader = (title: string, yPos: number, color: [number, number, number] = [74, 93, 35]) => {
      checkPageBreak(15);
      doc.setFont("helvetica", "bold");
      doc.setFontSize(11);
      doc.setTextColor(color[0], color[1], color[2]);
      doc.text(title, margin, yPos);
      return yPos + 5;
    };

    // Header
    doc.setFont("helvetica", "bold");
    doc.setFontSize(16);
    doc.setTextColor(44, 26, 20);
    doc.text("AyurNidana Clinical Protocol", margin, y);
    
    // Date & Name aligned right
    const dateStr = new Date().toLocaleString();
    doc.setFontSize(9);
    doc.setFont("helvetica", "normal");
    doc.text(dateStr, 210 - margin - doc.getTextWidth(dateStr), y);
    y += 10;

    // Diagnosis Section
    doc.setFontSize(12);
    doc.setTextColor(74, 93, 35);
    doc.setFont("helvetica", "bold");
    doc.text("Primary Diagnosis", margin, y);
    y += 6;
    
    doc.setFont("helvetica", "normal");
    doc.setFontSize(10);
    doc.setTextColor(0, 0, 0);
    doc.text(`${results.diagnosis.primary_condition} — ${results.diagnosis.sanskrit_name} (${results.diagnosis.doshic_subtype})`, margin, y);
    y += 8;

    // Doshas
    doc.setFont("helvetica", "bold");
    doc.setFontSize(10);
    doc.setTextColor(74, 93, 35);
    doc.text("Doshic Constitution:", margin, y);
    doc.setFont("helvetica", "normal");
    doc.setTextColor(0, 0, 0);
    doc.text(`Vata: ${Math.round(results.dosha_pct.Vata ?? 33)}% | Pitta: ${Math.round(results.dosha_pct.Pitta ?? 33)}% | Kapha: ${Math.round(results.dosha_pct.Kapha ?? 33)}%`, margin + 40, y);
    y += 10;

    if (results.treatment) {
      // Phase 1
      y = addSectionHeader("Phase 1: Nidana Parivarjana (Avoidance - Immediate)", y, [155, 44, 44]);
      doc.setFont("helvetica", "normal");
      doc.setFontSize(9);
      doc.setTextColor(0, 0, 0);
      const badHabits = [
        ...(results.treatment.dietary_and_lifestyle_regimen?.apathya_ahara_unwholesome_diet || []),
        ...(results.treatment.dietary_and_lifestyle_regimen?.apathya_vihara_contraindicated_habits || [])
      ];
      badHabits.forEach((h: string) => { checkPageBreak(5); y += addWrappedText(`• ${h}`, margin + 5, y, pageWidth - 10); });
      y += 4;

      // Phase 2
      if (results.treatment.deepana_pachana_protocol?.length > 0) {
        y = addSectionHeader("Phase 2: Agni Deepana & Ama Pachana (Metabolic Reset - 3-7 Days)", y, [194, 98, 43]);
        doc.setFont("helvetica", "normal"); doc.setFontSize(9); doc.setTextColor(0, 0, 0);
        results.treatment.deepana_pachana_protocol.forEach((p: string) => { checkPageBreak(5); y += addWrappedText(`• ${p}`, margin + 5, y, pageWidth - 10); });
        y += 4;
      }

      // Phase 3
      if (results.treatment.panchakarma_guidance?.eligible) {
        y = addSectionHeader("Phase 3: Shodhana (Deep Cleansing - 7-14 Days)", y);
        doc.setFont("helvetica", "normal"); doc.setFontSize(9); doc.setTextColor(0, 0, 0);
        y += addWrappedText(`Therapy: ${results.treatment.panchakarma_guidance.recommended_therapy}`, margin + 5, y, pageWidth - 10);
        y += addWrappedText(`Prep: ${results.treatment.panchakarma_guidance.purvakarma.join(', ')}`, margin + 5, y, pageWidth - 10);
        y += 4;
      }

      // Phase 4
      if (results.treatment.shamana_formulations?.length > 0) {
        y = addSectionHeader("Phase 4: Shamana (Herbal Medicine)", y);
        results.treatment.shamana_formulations.forEach((f: any) => {
          checkPageBreak(15);
          doc.setFont("helvetica", "bold"); doc.setFontSize(9); doc.setTextColor(0, 0, 0);
          doc.text(`• ${f.name} (${f.category}) — ${f.duration_weeks} Weeks`, margin + 5, y); y += 4.5;
          doc.setFont("helvetica", "normal"); doc.setFontSize(8.5); doc.setTextColor(60, 60, 60);
          doc.text(`Dosage: ${f.dosage} | Vehicle: ${f.anupana_vehicle} | Time: ${f.aushadha_sevana_kala}`, margin + 10, y); y += 6;
        });
        y += 2;
      }

      // Phase 5
      y = addSectionHeader("Phase 5: Pathya & Rasayana (Long-term Maintenance)", y);
      doc.setFont("helvetica", "normal"); doc.setFontSize(9); doc.setTextColor(0, 0, 0);
      const goodHabits = [
        ...(results.treatment.dietary_and_lifestyle_regimen?.pathya_ahara_wholesome_diet || []),
        ...(results.treatment.dietary_and_lifestyle_regimen?.pathya_vihara_recommended_lifestyle || []),
        ...(results.treatment.rasayana_recovery_plan || [])
      ];
      goodHabits.forEach((h: string) => { checkPageBreak(5); y += addWrappedText(`• ${h}`, margin + 5, y, pageWidth - 10); });
    }

    const patientName = user?.full_name || "Guest";
    const dateFormatted = new Date().toISOString().replace(/T/, '_').replace(/:/g, '').split('.')[0];
    const filename = `ayurnidana_${patientName.replace(/\s+/g, '_').toLowerCase()}_${dateFormatted}.pdf`;
    
    doc.save(filename);
  };

  return (
    <div className="min-h-screen bg-[#FDFBF7] text-[#2C1A14] font-[family-name:var(--font-nunito)] selection:bg-[#F2E5D5]">
      
      <style dangerouslySetInnerHTML={{__html: `
        .markdown-prose p { margin-bottom: 1em; }
        .markdown-prose ul { list-style-type: disc; padding-left: 1.5em; margin-bottom: 1em; }
        .markdown-prose ol { list-style-type: decimal; padding-left: 1.5em; margin-bottom: 1em; }
        .markdown-prose strong { font-weight: 700; color: #FDFBF7; }
        .markdown-prose li { margin-bottom: 0.5em; }
      `}} />

      {/* Header */}
      <header className="px-6 md:px-8 py-6 flex items-center justify-between border-b border-[#E8DCCB] bg-white/50 backdrop-blur-md sticky top-0 z-50">
        <div className="flex items-center gap-2 font-[family-name:var(--font-playfair)] font-medium text-2xl italic tracking-wide text-[#4A5D23] cursor-pointer hover:opacity-80 transition-opacity" onClick={() => setStep("WELCOME")}>
          <Leaf className="w-6 h-6" /> AyurNidana
        </div>
        <div className="flex items-center gap-4">
          {user ? (
            <>
              <button onClick={fetchHistory} className="text-[#8F7D74] hover:text-[#4A5D23] font-medium flex items-center gap-1 cursor-pointer transition-colors text-sm md:text-base"><History className="w-4 h-4"/> History</button>
              <button onClick={() => setUser(null)} className="text-[#8F7D74] hover:text-[#9B2C2C] font-medium flex items-center gap-1 cursor-pointer transition-colors text-sm md:text-base"><LogOut className="w-4 h-4"/> Logout</button>
            </>
          ) : (
            <button onClick={() => setStep("AUTH")} className="text-[#4A5D23] font-semibold flex items-center gap-1 cursor-pointer hover:opacity-80 transition-opacity text-sm md:text-base"><UserCircle className="w-4 h-4"/> Sign In</button>
          )}
        </div>
      </header>

      <main className="max-w-4xl mx-auto px-6 py-12 md:py-16">
        
        {/* WELCOME */}
        {step === "WELCOME" && (
          <div className="space-y-8 animate-in fade-in slide-in-from-bottom-8 duration-700 text-center flex flex-col items-center pt-10">
            <div className="w-24 h-24 bg-[#F2F5EB] rounded-full flex items-center justify-center mb-4 shadow-sm border border-[#E8DCCB]">
              <Sparkles className="w-10 h-10 text-[#4A5D23]" />
            </div>
            <h1 className="text-4xl md:text-5xl font-[family-name:var(--font-playfair)] text-[#2C1A14] leading-tight max-w-xl">
              Discover your body&apos;s innate wisdom.
            </h1>
            <p className="text-xl text-[#5B4A42] max-w-lg leading-relaxed">
              We combine classical Ayurvedic wisdom with modern intelligence to understand the root cause of your imbalances.
            </p>
            <Button onClick={() => setStep("INTAKE")} className="mt-8 cursor-pointer bg-[#4A5D23] hover:bg-[#3B4A1C] text-white text-xl px-10 py-8 rounded-full shadow-lg hover:scale-105 transition-all">
              Begin Consultation
            </Button>
          </div>
        )}

        {/* INTAKE / VITALS */}
        {step === "INTAKE" && (
          <div className="space-y-10 animate-in fade-in slide-in-from-right-8 duration-500 max-w-2xl mx-auto">
            <div className="space-y-4">
              <h2 className="text-4xl font-[family-name:var(--font-playfair)]">Patient Details</h2>
              <p className="text-xl text-[#5B4A42]">Tell us a bit about yourself so we can safely tailor the Ayurvedic protocol to your body type and existing conditions.</p>
            </div>
            
            <div className="space-y-6">
              <div>
                <label className="block text-lg font-semibold text-[#2C1A14] mb-2">Age</label>
                <input type="number" placeholder="e.g. 35" value={patientAge} onChange={(e) => setPatientAge(e.target.value)} className="w-full p-4 text-xl rounded-2xl border-2 border-[#E8DCCB] bg-white focus:border-[#4A5D23] focus:ring-0 shadow-sm outline-none" />
              </div>
              <div>
                <label className="block text-lg font-semibold text-[#2C1A14] mb-2">Existing Conditions / Comorbidities</label>
                <p className="text-sm text-[#8F7D74] mb-3">e.g. Diabetes, Hypothyroidism, PCOS, Hypertension. Knowing this helps us avoid prescribing incompatible herbs or sugars.</p>
                <Textarea placeholder="List any chronic conditions or allopathic diagnoses here..." value={comorbidities} onChange={(e) => setComorbidities(e.target.value)} className="w-full min-h-[120px] p-4 text-xl rounded-2xl border-2 border-[#E8DCCB] bg-white focus:border-[#4A5D23] focus:ring-0 resize-none shadow-sm outline-none" />
              </div>
            </div>

            <div className="flex justify-between items-center pt-4">
              <button onClick={() => setStep("WELCOME")} className="flex items-center gap-2 text-lg text-[#8F7D74] hover:text-[#2C1A14] cursor-pointer"><ArrowLeft className="w-5 h-5" /> Back</button>
              <Button onClick={() => setStep("COMPLAINT")} className="bg-[#4A5D23] cursor-pointer hover:bg-[#3B4A1C] text-white text-lg px-8 py-6 rounded-full transition-all shadow-md">Continue <ArrowRight className="ml-2 w-5 h-5" /></Button>
            </div>
          </div>
        )}

        {/* AUTH */}
        {step === "AUTH" && (
          <div className="max-w-md mx-auto bg-white p-8 rounded-3xl shadow-sm border border-[#E8DCCB] animate-in fade-in">
            <h2 className="text-3xl font-[family-name:var(--font-playfair)] text-center mb-6">{authMode === "LOGIN" ? "Welcome Back" : "Create Account"}</h2>
            <div className="space-y-4">
              {authMode === "REGISTER" && <input type="text" placeholder="Full Name" className="w-full p-4 rounded-xl border border-[#E8DCCB] focus:border-[#4A5D23] outline-none text-lg" value={authName} onChange={e=>setAuthName(e.target.value)} />}
              <input type="text" placeholder="Email / Username" className="w-full p-4 rounded-xl border border-[#E8DCCB] focus:border-[#4A5D23] outline-none text-lg" value={authIdent} onChange={e=>setAuthIdent(e.target.value)} />
              <input type="password" placeholder="Password" className="w-full p-4 rounded-xl border border-[#E8DCCB] focus:border-[#4A5D23] outline-none text-lg" value={authPass} onChange={e=>setAuthPass(e.target.value)} />
              <Button onClick={handleAuth} className="w-full cursor-pointer bg-[#4A5D23] hover:bg-[#3B4A1C] text-white h-14 rounded-xl text-xl transition-all">{authMode === "LOGIN" ? "Sign In" : "Register"}</Button>
              <p className="text-center text-[#8F7D74] mt-4 cursor-pointer hover:text-[#2C1A14] transition-colors" onClick={() => setAuthMode(authMode === "LOGIN" ? "REGISTER" : "LOGIN")}>
                {authMode === "LOGIN" ? "Need an account? Register" : "Already have an account? Sign In"}
              </p>
            </div>
          </div>
        )}

        {/* HISTORY */}
        {step === "HISTORY" && (
          <div className="space-y-8 animate-in fade-in">
            <h2 className="text-4xl font-[family-name:var(--font-playfair)] flex items-center gap-3"><History className="text-[#4A5D23] w-8 h-8"/> Your Healing Journey</h2>
            {historyList.length === 0 ? (
              <p className="text-xl text-[#8F7D74]">No past consultations found.</p>
            ) : (
              <div className="space-y-4">
                {historyList.map(h => (
                  <div key={h.id} 
                    onClick={() => {
                      if (h.case_sheet_md && h.case_sheet_md.startsWith('{')) {
                        try {
                          setResults(JSON.parse(h.case_sheet_md));
                          setStep("RESULTS");
                        } catch (e) {
                          alert("Could not load this consultation details.");
                        }
                      } else {
                        alert("Detailed record not available for this legacy consultation.");
                      }
                    }}
                    className="p-6 bg-white rounded-2xl border border-[#E8DCCB] shadow-sm hover:shadow-md transition-all flex justify-between items-center cursor-pointer">
                    <div>
                      <h3 className="text-2xl font-bold">{h.primary_condition}</h3>
                      <p className="text-[#8F7D74] text-lg mt-1">{new Date(h.created_at).toLocaleDateString()} — {h.sanskrit_name}</p>
                    </div>
                    <ArrowRight className="text-[#4A5D23] w-6 h-6" />
                  </div>
                ))}
              </div>
            )}
          </div>
        )}

        {/* COMPLAINT & SIGNALS */}
        {step === "COMPLAINT" && (
          <div className="space-y-8 animate-in fade-in slide-in-from-right-8 duration-500 max-w-3xl mx-auto">
            <div className="space-y-3 text-center">
              <h2 className="text-4xl font-[family-name:var(--font-playfair)]">What brings you here today?</h2>
              <p className="text-xl text-[#5B4A42]">Tell us your story in your own words, or tap a topic below to start.</p>
            </div>
            
            <div className="grid grid-cols-2 md:grid-cols-3 gap-4 mb-6">
                   <div className="flex flex-col items-center justify-center p-4 bg-[#F2F5EB] border border-[#E8DCCB] rounded-2xl">
                      <Moon className="w-7 h-7 text-[#4A5D23] mb-2" />
                      <span className="text-sm font-semibold text-[#2C1A14]">Sleep & Mental State</span>
                      <span className="text-xs text-[#8F7D74] text-center mt-1">Stress, anxiety, sleep quality</span>
                   </div>
                   <div className="flex flex-col items-center justify-center p-4 bg-[#FDF0EE] border border-[#E8DCCB] rounded-2xl">
                      <Activity className="w-7 h-7 text-[#9B2C2C] mb-2" />
                      <span className="text-sm font-semibold text-[#2C1A14]">Pain & Discomfort</span>
                      <span className="text-xs text-[#8F7D74] text-center mt-1">Location, intensity, onset</span>
                   </div>
                   <div className="flex flex-col items-center justify-center p-4 bg-[#FCF9F2] border border-[#E8DCCB] rounded-2xl">
                      <Utensils className="w-7 h-7 text-[#C2622B] mb-2" />
                      <span className="text-sm font-semibold text-[#2C1A14]">Digestion & Appetite</span>
                      <span className="text-xs text-[#8F7D74] text-center mt-1">Bloating, acidity, cravings</span>
                   </div>
                   <div className="flex flex-col items-center justify-center p-4 bg-[#FDFBF7] border border-[#E8DCCB] rounded-2xl">
                      <Clock className="w-7 h-7 text-[#5B4A42] mb-2" />
                      <span className="text-sm font-semibold text-[#2C1A14]">Timing / Aggravation</span>
                      <span className="text-xs text-[#8F7D74] text-center mt-1">When do symptoms worsen?</span>
                   </div>
                   <div className="flex flex-col items-center justify-center p-4 bg-[#FDF0EE] border border-[#E8DCCB] rounded-2xl">
                      <Droplets className="w-7 h-7 text-[#2B6CB0] mb-2" />
                      <span className="text-sm font-semibold text-[#2C1A14]">Bowel Movements</span>
                      <span className="text-xs text-[#8F7D74] text-center mt-1">Constipation, loose stools</span>
                   </div>
                   <div className="flex flex-col items-center justify-center p-4 bg-[#F2F5EB] border border-[#E8DCCB] rounded-2xl">
                      <HeartPulse className="w-7 h-7 text-[#E53E3E] mb-2" />
                      <span className="text-sm font-semibold text-[#2C1A14]">Energy Levels</span>
                      <span className="text-xs text-[#8F7D74] text-center mt-1">Fatigue, stamina changes</span>
                   </div>
                </div>
    
                <Textarea placeholder="e.g., I've been feeling deeply exhausted lately..." value={story} onChange={(e) => setStory(e.target.value)} className="w-full min-h-[180px] p-6 text-xl rounded-3xl border-2 border-[#E8DCCB] bg-white focus:border-[#4A5D23] focus:ring-0 resize-none shadow-sm" />
            
            <div className="flex justify-between items-center">
              <button onClick={() => setStep("INTAKE")} className="flex items-center gap-2 text-lg text-[#8F7D74] hover:text-[#2C1A14] cursor-pointer"><ArrowLeft className="w-5 h-5" /> Back</button>
              <Button onClick={() => story.trim() ? setStep("SIGNALS") : alert("Please share your story.")} className="bg-[#4A5D23] cursor-pointer hover:bg-[#3B4A1C] text-white text-lg px-8 py-6 rounded-full transition-all shadow-md">Continue <ArrowRight className="ml-2 w-5 h-5" /></Button>
            </div>
          </div>
        )}

        {step === "SIGNALS" && (
          <div className="space-y-10 animate-in fade-in slide-in-from-right-8 duration-500">
            <h2 className="text-4xl font-[family-name:var(--font-playfair)]">Your Body&apos;s Signals</h2>
            <div className="space-y-12">
              {[{title:"1. Tongue in the morning", opts:TONGUE_OPTS, val:tongue, set:setTongue}, {title:"2. Bowel movements", opts:STOOL_OPTS, val:stool, set:setStool}, {title:"3. Appetite", opts:HUNGER_OPTS, val:hunger, set:setHunger}].map((group, idx) => (
                <div key={idx} className="space-y-6">
                  <h3 className="font-semibold text-2xl text-[#2C1A14]">{group.title}</h3>
                  <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-4 gap-4">
                    {group.opts.map(o => (
                      <button key={o.val} onClick={() => group.set(o.val)} className={`cursor-pointer p-5 text-left rounded-2xl border-2 transition-all ${group.val === o.val ? "border-[#4A5D23] bg-[#F2F5EB] shadow-md scale-[1.02]" : "border-[#E8DCCB] bg-white hover:border-[#4A5D23]"}`}>
                        <div className={`font-semibold text-lg ${group.val === o.val ? "text-[#3B4A1C]" : ""}`}>{o.label}</div>
                        <div className="text-base mt-1 text-[#8F7D74]">{o.sub}</div>
                      </button>
                    ))}
                  </div>
                </div>
              ))}
            </div>
            <div className="flex flex-col sm:flex-row justify-between items-center gap-6 pt-10 border-t border-[#E8DCCB]">
              <button onClick={() => setStep("COMPLAINT")} className="flex items-center gap-2 text-lg text-[#8F7D74] hover:text-[#2C1A14] cursor-pointer"><ArrowLeft className="w-5 h-5" /> Back</button>
              <Button onClick={handleRunConsultation} className="w-full sm:w-auto bg-[#4A5D23] cursor-pointer hover:bg-[#3B4A1C] text-white text-lg px-10 py-8 rounded-full transition-all">Synthesize Plan <Sparkles className="ml-2 w-5 h-5" /></Button>
            </div>
          </div>
        )}

        {step === "LOADING" && (
          <div className="py-32 flex flex-col items-center space-y-8">
            <div className="w-24 h-24 border-4 border-[#4A5D23] border-t-transparent rounded-full animate-spin flex items-center justify-center"><Leaf className="w-8 h-8 text-[#4A5D23] animate-pulse" /></div>
            <h3 className="text-3xl font-[family-name:var(--font-playfair)]">Synthesizing Blueprint...</h3>
          </div>
        )}

        {step === "RESULTS" && results && (
          <div className="space-y-12 animate-in fade-in pb-20">
            
            <div className="flex justify-end mb-4">
              <Button onClick={downloadPDF} variant="outline" className="cursor-pointer border-[#4A5D23] text-[#4A5D23] hover:bg-[#F2F5EB] rounded-full text-lg h-12 px-6">
                <Printer className="w-5 h-5 mr-2" /> Download PDF Prescription
              </Button>
            </div>
            
            {/* WRAP CONTENT TO PRINT IN DIV */}
            <div id="pdf-content" className="space-y-12">
            
              <div className="text-center space-y-4">
                <div className="inline-flex items-center gap-2 px-5 py-2 rounded-full bg-[#F2F5EB] text-[#4A5D23] text-sm font-semibold uppercase tracking-widest"><HeartPulse className="w-5 h-5" /> Primary Diagnosis</div>
                <h2 className="text-5xl md:text-6xl font-[family-name:var(--font-playfair)]">{results.diagnosis.primary_condition}</h2>
                <p className="text-2xl text-[#8F7D74] font-[family-name:var(--font-playfair)] italic">{results.diagnosis.sanskrit_name} ({results.diagnosis.doshic_subtype})</p>
              </div>

              {results.diagnosis.clinical_reasoning && (
                <div className="bg-[#FCF9F2] rounded-3xl p-8 md:p-10 border border-[#E8DCCB]">
                  <h3 className="text-3xl font-[family-name:var(--font-playfair)] mb-6 flex items-center gap-3"><BookOpen className="w-8 h-8 text-[#4A5D23]" /> Pathogenesis (Samprapti)</h3>
                  <p className="text-[#5B4A42] leading-relaxed text-xl">{results.diagnosis.clinical_reasoning}</p>
                  <div className="mt-6 flex flex-wrap gap-4 text-base">
                    <span className="bg-white border px-4 py-2 rounded-lg"><strong>Agni:</strong> {String(results.agni).split('(')[0].trim()}</span>
                    <span className="bg-white border px-4 py-2 rounded-lg"><strong>Ama:</strong> {String(results.ama_status).split('(')[0].trim()}</span>
                  </div>
                </div>
              )}

              <div className="bg-white rounded-[2rem] p-8 md:p-12 shadow-sm border border-[#E8DCCB]">
                 <h3 className="text-3xl font-[family-name:var(--font-playfair)] mb-10 text-center">Your Doshic Constitution</h3>
                 <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
                   {[{name:"Vata", icon:Wind, bg:"bg-[#F0F6F9]", fill:"bg-[#3182CE]", text:"text-[#2C5282]", val:Math.round(results.dosha_pct.Vata ?? 33)},
                     {name:"Pitta", icon:Flame, bg:"bg-[#FDF0EE]", fill:"bg-[#E53E3E]", text:"text-[#9B2C2C]", val:Math.round(results.dosha_pct.Pitta ?? 33)},
                     {name:"Kapha", icon:Droplets, bg:"bg-[#F2F5EB]", fill:"bg-[#38A169]", text:"text-[#276749]", val:Math.round(results.dosha_pct.Kapha ?? 33)}].map(d => (
                     <div key={d.name} className="flex flex-col items-center space-y-4">
                       <div className={`w-20 h-20 rounded-full ${d.bg} ${d.text} flex items-center justify-center`}><d.icon className="w-10 h-10" /></div>
                       <h4 className="font-semibold text-2xl">{d.name}</h4>
                       <div className={`w-full h-3 ${d.bg} rounded-full overflow-hidden`}><div className={`h-full ${d.fill}`} style={{width: `${d.val}%`}}></div></div>
                       <span className={`${d.text} font-bold text-xl`}>{d.val}%</span>
                     </div>
                   ))}
                 </div>
              </div>

              <div className="space-y-12 pt-8">
                <h3 className="text-4xl font-[family-name:var(--font-playfair)] text-center">Clinical Protocol</h3>
                
                {/* Phase 1: Nidana Parivarjana */}
                <div className="bg-[#FDF0EE] rounded-3xl p-8 border border-[#E8DCCB]">
                  <div className="mb-6">
                    <h4 className="text-[#9B2C2C] font-bold text-2xl flex items-center gap-3"><XCircle className="w-7 h-7" /> Phase 1: Nidana Parivarjana (Avoidance)</h4>
                    <span className="text-[#E53E3E] text-sm font-semibold tracking-wider uppercase">Duration: Immediate & Continuous</span>
                  </div>
                  <ul className="space-y-3 text-lg">
                    {[...(results.treatment.dietary_and_lifestyle_regimen?.apathya_ahara_unwholesome_diet || []), ...(results.treatment.dietary_and_lifestyle_regimen?.apathya_vihara_contraindicated_habits || [])].map((item: string, i: number) => (
                      <li key={i} className="flex gap-3"><span className="text-[#E53E3E] shrink-0 mt-1">•</span> <span className="text-[#2C1A14]">{item}</span></li>
                    ))}
                  </ul>
                </div>

                {/* Phase 2: Agni Deepana */}
                {results.treatment.deepana_pachana_protocol && results.treatment.deepana_pachana_protocol.length > 0 && (
                  <div className="bg-[#FCF9F2] rounded-3xl p-8 border border-[#E8DCCB]">
                    <div className="mb-6">
                      <h4 className="text-[#C2622B] font-bold text-2xl flex items-center gap-3"><Flame className="w-7 h-7" /> Phase 2: Agni Deepana & Ama Pachana</h4>
                      <span className="text-[#C2622B] text-sm font-semibold tracking-wider uppercase">Duration: First 3 - 7 Days (Metabolic Reset)</span>
                    </div>
                    <ul className="space-y-3 text-lg">
                      {results.treatment.deepana_pachana_protocol.map((item: string, i: number) => (
                        <li key={i} className="flex gap-3"><span className="text-[#C2622B] shrink-0 mt-1">•</span> <span className="text-[#2C1A14]">{item}</span></li>
                      ))}
                    </ul>
                  </div>
                )}

                {/* Phase 3: Shodhana */}
                {results.treatment.panchakarma_guidance?.eligible && (
                  <div className="bg-[#F2F5EB] rounded-3xl p-8 border border-[#E8DCCB]">
                    <div className="mb-6">
                      <h4 className="text-[#276749] font-bold text-2xl flex items-center gap-3"><Activity className="w-7 h-7"/> Phase 3: Shodhana (Deep Cleansing)</h4>
                      <span className="text-[#276749] text-sm font-semibold tracking-wider uppercase">Duration: As advised by physician (Approx 7-14 Days)</span>
                    </div>
                    <div className="space-y-3">
                      <p className="text-[#2C1A14] text-xl font-medium">Recommended: {results.treatment.panchakarma_guidance.recommended_therapy}</p>
                      <p className="text-[#5B4A42] text-lg">{results.treatment.panchakarma_guidance.reasoning}</p>
                      <p className="text-[#8F7D74] italic">Preparation (Purvakarma): {results.treatment.panchakarma_guidance.purvakarma.join(', ')}</p>
                    </div>
                  </div>
                )}

                {/* Phase 4: Shamana */}
                {results.treatment.shamana_formulations && results.treatment.shamana_formulations.length > 0 && (
                  <div className="space-y-6">
                    <div className="mb-2">
                      <h4 className="text-[#4A5D23] font-bold text-2xl flex items-center gap-3"><Leaf className="w-7 h-7"/> Phase 4: Shamana (Herbal Medicine)</h4>
                      <span className="text-[#4A5D23] text-sm font-semibold tracking-wider uppercase ml-10">Duration: As prescribed below</span>
                    </div>
                    <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                      {results.treatment.shamana_formulations.map((f:any, i:number) => (
                        <div key={i} className="bg-white rounded-3xl p-8 border border-[#E8DCCB] flex flex-col justify-between">
                          <div className="mb-6">
                            <h5 className="text-2xl font-bold flex flex-wrap items-center gap-3">{f.name} <span className="text-sm bg-[#F2F5EB] text-[#4A5D23] px-3 py-1 rounded-full">{f.category}</span></h5>
                            <p className="text-[#8F7D74] text-lg italic mt-3">{f.classical_indication}</p>
                          </div>
                          <div className="bg-[#FCF9F2] rounded-2xl p-5 text-lg space-y-4 border border-[#E8DCCB]">
                            <div className="flex gap-4 items-center text-[#2C1A14] font-medium"><Activity className="w-5 h-5 text-[#4A5D23] shrink-0"/> Duration: {f.duration_weeks} Weeks</div>
                            <div className="flex gap-4 items-center"><Pill className="w-5 h-5 text-[#4A5D23] shrink-0"/> Dosage: {f.dosage}</div>
                            <div className="flex gap-4 items-center"><GlassWater className="w-5 h-5 text-[#4A5D23] shrink-0"/> Vehicle: {f.anupana_vehicle}</div>
                            <div className="flex gap-4 items-center"><Clock className="w-5 h-5 text-[#4A5D23] shrink-0"/> Timing: {f.aushadha_sevana_kala}</div>
                          </div>
                        </div>
                      ))}
                    </div>
                  </div>
                )}

                {/* Phase 5: Pathya & Rasayana */}
                <div className="bg-white rounded-3xl p-8 border border-[#E8DCCB] shadow-sm">
                  <div className="mb-6">
                    <h4 className="text-[#2C1A14] font-bold text-2xl flex items-center gap-3"><CheckCircle2 className="w-7 h-7 text-[#4A5D23]" /> Phase 5: Pathya & Rasayana (Nourishment)</h4>
                    <span className="text-[#8F7D74] text-sm font-semibold tracking-wider uppercase ml-10">Duration: Long-term Maintenance</span>
                  </div>
                  <ul className="space-y-3 text-lg">
                    {[
                      ...(results.treatment.dietary_and_lifestyle_regimen?.pathya_ahara_wholesome_diet || []), 
                      ...(results.treatment.dietary_and_lifestyle_regimen?.pathya_vihara_recommended_lifestyle || []),
                      ...(results.treatment.rasayana_recovery_plan || [])
                    ].map((item: string, i: number) => (
                      <li key={i} className="flex gap-3"><span className="text-[#4A5D23] shrink-0 mt-1">•</span> <span className="text-[#2C1A14]">{item}</span></li>
                    ))}
                  </ul>
                </div>

              </div>
            </div>

            <div className="mt-16 bg-[#2C1A14] rounded-[2rem] p-8 md:p-12 text-[#FDFBF7] shadow-xl">
               <h3 className="font-[family-name:var(--font-playfair)] text-3xl mb-6 flex gap-3 items-center"><Stethoscope className="text-[#E8DCCB] w-8 h-8" /> Ask AyurVaidya</h3>
               <div className="space-y-6">
                 <Textarea placeholder="e.g. Can I drink coffee while taking these herbs?" className="w-full bg-[#43302B] border-none text-white focus:ring-[#4A5D23] min-h-[120px] text-xl p-6 rounded-2xl resize-none" value={chatQ} onChange={e=>setChatQ(e.target.value)} />
                 <Button onClick={handleChat} disabled={isChatLoading || !chatQ.trim()} className="w-full bg-[#4A5D23] cursor-pointer hover:bg-[#3B4A1C] text-white h-14 text-xl rounded-full">Send Question</Button>
                 {chatA && <div className="p-6 md:p-8 bg-[#43302B] rounded-2xl text-lg markdown-prose"><ReactMarkdown remarkPlugins={[remarkGfm]}>{chatA}</ReactMarkdown></div>}
               </div>
            </div>

          </div>
        )}
      </main>
    </div>
  );
}
