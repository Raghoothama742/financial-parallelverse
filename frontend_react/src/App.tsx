import React, { useState, useEffect } from 'react';
import { api } from './lib/api';
import { FinancialProfile, ScenarioSimulationResponse, PurchaseEvaluationResponse } from './types';

export default function App() {
  const [profile, setProfile] = useState<FinancialProfile | null>(null);
  const [activeTab, setActiveTab] = useState<'overview' | 'simulator' | 'purchases' | 'emi' | 'installments' | 'profile'>('overview');
  const [loading, setLoading] = useState(true);
  const [simResults, setSimResults] = useState<ScenarioSimulationResponse | null>(null);
  const [purchaseResults, setPurchaseResults] = useState<PurchaseEvaluationResponse | null>(null);
  const [installments, setInstallments] = useState<any[]>([]);

  useEffect(() => {
    loadData();
  }, []);

  const loadData = async () => {
    try {
      setLoading(true);
      const prof = await api.getProfile();
      setProfile(prof);

      const sim = await api.simulateScenarios({
        duration_months: 12,
        purchase_name: prof.planned_purchase_name,
        purchase_amount: prof.planned_purchase_amount,
        purchase_mode: 'EMI'
      });
      setSimResults(sim);

      const purch = await api.evaluatePurchase({
        purchase_name: prof.planned_purchase_name,
        purchase_amount: prof.planned_purchase_amount,
        cheaper_alternative_amount: 42000,
        wait_months: 4
      });
      setPurchaseResults(purch);

      const inst = await api.getInstallments();
      setInstallments(inst);
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={{ display: 'flex', minHeight: '100vh', backgroundColor: '#060913', color: '#f8fafc', fontFamily: "'Plus Jakarta Sans', system-ui, sans-serif" }}>
      {/* Sidebar Navigation */}
      <aside style={{ width: '280px', backgroundColor: '#090e1a', borderRight: '1px solid rgba(255,255,255,0.08)', padding: '1.75rem 1.25rem', display: 'flex', flexDirection: 'column' }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: '14px', marginBottom: '2.5rem' }}>
          <div style={{ width: '46px', height: '46px', borderRadius: '14px', background: 'linear-gradient(135deg, #3b82f6 0%, #8b5cf6 50%, #10b981 100%)', display: 'flex', alignItems: 'center', justifyContent: 'center', fontSize: '1.7rem', boxShadow: '0 4px 18px rgba(59, 130, 246, 0.4)' }}>
            🌌
          </div>
          <div>
            <div style={{ fontSize: '1.25rem', fontWeight: 800, color: '#ffffff', letterSpacing: '-0.02em' }}>Parallelverse</div>
            <div style={{ fontSize: '0.72rem', color: '#38bdf8', fontWeight: 700, textTransform: 'uppercase' }}>FinTech Simulation</div>
          </div>
        </div>

        <nav style={{ display: 'flex', flexDirection: 'column', gap: '0.5rem', flex: 1 }}>
          {[
            { id: 'overview', label: '📊 Executive Overview', color: '#38bdf8' },
            { id: 'simulator', label: '🔮 Parallel Futures', color: '#a855f7' },
            { id: 'purchases', label: '⚖️ Purchase Matrix', color: '#34d399' },
            { id: 'emi', label: '🧮 EMI Calculator', color: '#fb923c' },
            { id: 'installments', label: '📅 Installment Tracker', color: '#f43f5e' },
            { id: 'profile', label: '👤 Financial Profile', color: '#38bdf8' }
          ].map((tab) => {
            const isActive = activeTab === tab.id;
            return (
              <button
                key={tab.id}
                onClick={() => setActiveTab(tab.id as any)}
                style={{
                  textAlign: 'left',
                  padding: '0.85rem 1.15rem',
                  borderRadius: '12px',
                  border: 'none',
                  cursor: 'pointer',
                  fontWeight: 700,
                  fontSize: '0.92rem',
                  backgroundColor: isActive ? 'rgba(56, 189, 248, 0.12)' : 'transparent',
                  color: isActive ? tab.color : '#94a3b8',
                  borderLeft: isActive ? `3px solid ${tab.color}` : '3px solid transparent',
                  boxShadow: isActive ? '0 4px 20px rgba(0,0,0,0.2)' : 'none',
                  transition: 'all 0.2s ease'
                }}
              >
                {tab.label}
              </button>
            );
          })}
        </nav>

        {profile && (
          <div style={{ backgroundColor: 'rgba(255,255,255,0.03)', border: '1px solid rgba(255,255,255,0.06)', borderRadius: '14px', padding: '1rem', fontSize: '0.82rem' }}>
            <div style={{ color: '#38bdf8', fontSize: '0.7rem', fontWeight: 800, textTransform: 'uppercase' }}>Active Persona</div>
            <div style={{ color: '#ffffff', fontWeight: 800, fontSize: '1rem', margin: '0.2rem 0 0.5rem 0' }}>{profile.full_name}</div>
            <div style={{ display: 'flex', justifyContent: 'space-between', color: '#94a3b8' }}>
              <span>Monthly Inflow:</span>
              <strong style={{ color: '#ffffff' }}>₹{profile.monthly_income.toLocaleString()}</strong>
            </div>
            <div style={{ display: 'flex', justifyContent: 'space-between', color: '#94a3b8', marginTop: '0.3rem' }}>
              <span>Liquid Reserve:</span>
              <strong style={{ color: '#34d399' }}>₹{profile.current_savings.toLocaleString()}</strong>
            </div>
          </div>
        )}
      </aside>

      {/* Main Content Area */}
      <main style={{ flex: 1, padding: '2.5rem', overflowY: 'auto', background: 'radial-gradient(circle at 10% 10%, #0e172a 0%, #080c17 45%, #050811 100%)' }}>
        {loading ? (
          <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'center', height: '100%', color: '#94a3b8' }}>
            Loading Financial Parallelverse...
          </div>
        ) : (
          <div>
            {/* Top Status Bar */}
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '1.5rem', padding: '0.65rem 1.25rem', background: 'linear-gradient(90deg, rgba(16, 185, 129, 0.12) 0%, rgba(6, 182, 212, 0.12) 50%, rgba(99, 102, 241, 0.12) 100%)', border: '1px solid rgba(16, 185, 129, 0.25)', borderRadius: '12px' }}>
              <div style={{ display: 'flex', alignItems: 'center', gap: '8px', fontSize: '0.85rem', fontWeight: 700, color: '#34d399' }}>
                <span style={{ width: '8px', height: '8px', borderRadius: '50%', backgroundColor: '#34d399', display: 'inline-block' }}></span>
                Deterministic Financial Engine &bull; Dual-Mode Live
              </div>
              <div style={{ display: 'flex', gap: '15px', fontSize: '0.8rem', color: '#94a3b8' }}>
                <span>Backend: <b style={{ color: '#34d399' }}>FastAPI :8000</b></span>
                <span>Storage: <b style={{ color: '#38bdf8' }}>SQLite 3</b></span>
                <span>Reminders: <b style={{ color: '#fb923c' }}>RFC 5545 iCal</b></span>
              </div>
            </div>

            {/* Hero Section on Overview */}
            {activeTab === 'overview' && (
              <div style={{ background: 'linear-gradient(135deg, rgba(30, 41, 59, 0.7) 0%, rgba(15, 23, 42, 0.9) 100%)', border: '1px solid rgba(255, 255, 255, 0.1)', borderRadius: '24px', padding: '2.5rem', marginBottom: '2rem', position: 'relative', overflow: 'hidden' }}>
                <div style={{ display: 'inline-flex', alignItems: 'center', gap: '8px', background: 'rgba(16, 185, 129, 0.18)', border: '1px solid rgba(16, 185, 129, 0.4)', padding: '0.35rem 0.9rem', borderRadius: '9999px', fontSize: '0.75rem', fontWeight: 800, color: '#34d399', textTransform: 'uppercase', marginBottom: '1rem' }}>
                  FinTech Stress Testing Engine &bull; Hack-o-Ween PESU
                </div>
                <h1 style={{ fontSize: '2.8rem', fontWeight: 800, lineHeight: 1.15, background: 'linear-gradient(135deg, #ffffff 10%, #38bdf8 45%, #a855f7 75%, #34d399 100%)', WebkitBackgroundClip: 'text', WebkitTextFillColor: 'transparent', margin: '0 0 0.75rem 0' }}>
                  Simulate Your Tomorrow Before Spending Today.
                </h1>
                <p style={{ color: '#94a3b8', fontSize: '1.05rem', maxWidth: '650px', lineHeight: 1.5, margin: '0 0 1.5rem 0' }}>
                  Simulates multiple parallel futures under adverse life shocks—salary delays, medical emergencies, and inflation—so you never commit blind.
                </p>
              </div>
            )}

            {/* 4 Glowing KPI Metric Cards */}
            {profile && (
              <div style={{ display: 'grid', gridTemplateColumns: 'repeat(4, 1fr)', gap: '1.25rem', marginBottom: '2rem' }}>
                <div style={{ background: 'linear-gradient(135deg, rgba(19, 29, 49, 0.8) 0%, rgba(13, 20, 36, 0.9) 100%)', border: '1px solid rgba(255,255,255,0.08)', borderTop: '3px solid #10b981', borderRadius: '20px', padding: '1.4rem' }}>
                  <div style={{ color: '#94a3b8', fontSize: '0.75rem', fontWeight: 700, textTransform: 'uppercase' }}>Monthly Free Cash Flow</div>
                  <div style={{ fontSize: '2.1rem', fontWeight: 800, color: profile.free_cash_flow < 0 ? '#fb7185' : '#34d399', marginTop: '0.3rem' }}>
                    ₹{profile.free_cash_flow.toLocaleString()}
                  </div>
                  <div style={{ fontSize: '0.8rem', color: '#38bdf8', marginTop: '0.5rem' }}>Savings Rate: <b>{profile.savings_rate_pct.toFixed(1)}%</b></div>
                </div>

                <div style={{ background: 'linear-gradient(135deg, rgba(19, 29, 49, 0.8) 0%, rgba(13, 20, 36, 0.9) 100%)', border: '1px solid rgba(255,255,255,0.08)', borderTop: '3px solid #06b6d4', borderRadius: '20px', padding: '1.4rem' }}>
                  <div style={{ color: '#94a3b8', fontSize: '0.75rem', fontWeight: 700, textTransform: 'uppercase' }}>Liquid Cash Reserves</div>
                  <div style={{ fontSize: '2.1rem', fontWeight: 800, color: '#ffffff', marginTop: '0.3rem' }}>
                    ₹{profile.current_savings.toLocaleString()}
                  </div>
                  <div style={{ fontSize: '0.8rem', color: '#34d399', marginTop: '0.5rem' }}>Emergency Buffer Target: <b>₹{profile.emergency_fund_target.toLocaleString()}</b></div>
                </div>

                <div style={{ background: 'linear-gradient(135deg, rgba(19, 29, 49, 0.8) 0%, rgba(13, 20, 36, 0.9) 100%)', border: '1px solid rgba(255,255,255,0.08)', borderTop: '3px solid #a855f7', borderRadius: '20px', padding: '1.4rem' }}>
                  <div style={{ color: '#94a3b8', fontSize: '0.75rem', fontWeight: 700, textTransform: 'uppercase' }}>Emergency Runway</div>
                  <div style={{ fontSize: '2.1rem', fontWeight: 800, color: '#ffffff', marginTop: '0.3rem' }}>
                    {profile.months_of_runway.toFixed(1)} <span style={{ fontSize: '1rem', color: '#94a3b8' }}>Mo</span>
                  </div>
                  <div style={{ fontSize: '0.8rem', color: '#38bdf8', marginTop: '0.5rem' }}>Survival without salary</div>
                </div>

                <div style={{ background: 'linear-gradient(135deg, rgba(19, 29, 49, 0.8) 0%, rgba(13, 20, 36, 0.9) 100%)', border: '1px solid rgba(255,255,255,0.08)', borderTop: '3px solid #f97316', borderRadius: '20px', padding: '1.4rem' }}>
                  <div style={{ color: '#94a3b8', fontSize: '0.75rem', fontWeight: 700, textTransform: 'uppercase' }}>Debt-to-Income (DTI)</div>
                  <div style={{ fontSize: '2.1rem', fontWeight: 800, color: profile.debt_to_income_pct > 35 ? '#fb7185' : '#34d399', marginTop: '0.3rem' }}>
                    {profile.debt_to_income_pct.toFixed(1)}%
                  </div>
                  <div style={{ fontSize: '0.8rem', color: '#94a3b8', marginTop: '0.5rem' }}>Safe Target: &lt; 35%</div>
                </div>
              </div>
            )}

            {/* Parallel Futures Grid */}
            {activeTab === 'simulator' && simResults && (
              <div>
                <h3 style={{ fontSize: '1.3rem', fontWeight: 800, marginBottom: '1.2rem', color: '#ffffff' }}>
                  🌌 5 Parallel Futures Simulation Matrix
                </h3>
                <div style={{ display: 'grid', gridTemplateColumns: 'repeat(5, 1fr)', gap: '1.1rem' }}>
                  {Object.entries(simResults.scenarios).map(([key, sc]) => {
                    const colorsMap: any = {
                      baseline: { border: '#10b981', tag: '#34d399', bg: 'rgba(16, 185, 129, 0.15)' },
                      unexpected_expense: { border: '#f97316', tag: '#fb923c', bg: 'rgba(249, 115, 22, 0.15)' },
                      delayed_salary: { border: '#06b6d4', tag: '#38bdf8', bg: 'rgba(6, 182, 212, 0.15)' },
                      increased_spending: { border: '#a855f7', tag: '#c084fc', bg: 'rgba(168, 85, 247, 0.15)' },
                      combined_adverse: { border: '#f43f5e', tag: '#fb7185', bg: 'rgba(244, 63, 94, 0.15)' }
                    };
                    const c = colorsMap[key] || colorsMap.baseline;
                    return (
                      <div key={key} style={{ background: 'linear-gradient(135deg, rgba(18, 26, 43, 0.85) 0%, rgba(11, 16, 28, 0.95) 100%)', border: '1px solid rgba(255,255,255,0.08)', borderTop: `4px solid ${c.border}`, borderRadius: '18px', padding: '1.35rem 1.25rem', minHeight: '300px', display: 'flex', flexDirection: 'column', justifyContent: 'space-between' }}>
                        <div>
                          <div style={{ fontWeight: 800, fontSize: '1rem', color: '#ffffff' }}>{sc.scenario_name}</div>
                          <span style={{ display: 'inline-block', marginTop: '0.4rem', padding: '0.2rem 0.6rem', borderRadius: '9999px', fontSize: '0.68rem', fontWeight: 800, backgroundColor: c.bg, color: c.tag, border: `1px solid ${c.border}` }}>
                            {sc.risk_level} RISK
                          </span>
                        </div>
                        <div style={{ margin: '1rem 0', background: 'rgba(255,255,255,0.02)', border: '1px solid rgba(255,255,255,0.05)', borderRadius: '12px', padding: '0.75rem' }}>
                          <div style={{ fontSize: '0.7rem', color: '#94a3b8', textTransform: 'uppercase' }}>Lowest Point</div>
                          <div style={{ fontSize: '1.4rem', fontWeight: 800, color: sc.lowest_savings < 0 ? '#fb7185' : '#ffffff' }}>
                            ₹{sc.lowest_savings.toLocaleString()}
                          </div>
                        </div>
                        <div style={{ fontSize: '0.78rem', color: '#94a3b8' }}>
                          <div>Resilience: <b style={{ color: '#ffffff' }}>{sc.resilience_score}/100</b></div>
                          <div>Deficit Months: <b style={{ color: sc.negative_cash_months > 0 ? '#fb7185' : '#34d399' }}>{sc.negative_cash_months}</b></div>
                        </div>
                        <div style={{ fontSize: '0.73rem', color: '#cbd5e1', borderTop: '1px solid rgba(255,255,255,0.08)', paddingTop: '0.5rem', marginTop: '0.5rem' }}>
                          {sc.breaking_point_reason}
                        </div>
                      </div>
                    );
                  })}
                </div>
              </div>
            )}

            {/* Purchase Matrix */}
            {activeTab === 'purchases' && purchaseResults && (
              <div>
                <h3 style={{ fontSize: '1.3rem', fontWeight: 800, marginBottom: '1.2rem', color: '#ffffff' }}>
                  ⚖️ Purchase Pathway Decision Matrix
                </h3>
                <div style={{ display: 'grid', gridTemplateColumns: 'repeat(4, 1fr)', gap: '1.25rem' }}>
                  {purchaseResults.options.map((opt) => {
                    const isRec = opt.option_id === purchaseResults.recommended_option_id;
                    return (
                      <div key={opt.option_id} style={{ background: 'linear-gradient(135deg, rgba(18, 27, 46, 0.85) 0%, rgba(10, 16, 28, 0.95) 100%)', borderRadius: '20px', padding: '1.6rem 1.4rem', border: isRec ? '2px solid #10b981' : '1px solid rgba(255,255,255,0.08)', position: 'relative' }}>
                        {isRec && (
                          <div style={{ position: 'absolute', top: '1rem', right: '1rem', background: 'linear-gradient(90deg, #10b981 0%, #06b6d4 100%)', color: '#041a11', fontWeight: 800, fontSize: '0.68rem', textTransform: 'uppercase', padding: '0.2rem 0.6rem', borderRadius: '9999px' }}>
                            ⭐ Best Fit
                          </div>
                        )}
                        <div style={{ fontWeight: 800, fontSize: '1.15rem', color: '#ffffff', marginBottom: '0.5rem' }}>{opt.option_title}</div>
                        <span style={{ display: 'inline-block', padding: '0.25rem 0.65rem', borderRadius: '9999px', fontSize: '0.68rem', fontWeight: 800, textTransform: 'uppercase', backgroundColor: opt.risk_rating === 'SAFE' ? 'rgba(16,185,129,0.15)' : 'rgba(244,63,94,0.15)', color: opt.risk_rating === 'SAFE' ? '#34d399' : '#fb7185' }}>
                          {opt.risk_rating}
                        </span>

                        <div style={{ margin: '1.2rem 0 0.8rem 0', borderTop: '1px solid rgba(255,255,255,0.08)', paddingTop: '0.8rem' }}>
                          <div style={{ fontSize: '0.72rem', color: '#94a3b8', textTransform: 'uppercase' }}>Upfront Cash Required</div>
                          <div style={{ fontSize: '1.4rem', fontWeight: 800, color: '#ffffff' }}>₹{opt.upfront_cash_required.toLocaleString()}</div>
                        </div>

                        <div style={{ marginBottom: '0.8rem' }}>
                          <div style={{ fontSize: '0.72rem', color: '#94a3b8', textTransform: 'uppercase' }}>Monthly Obligation</div>
                          <div style={{ fontSize: '1.4rem', fontWeight: 800, color: '#38bdf8' }}>₹{opt.monthly_obligation.toLocaleString()}/mo</div>
                        </div>

                        <div style={{ marginBottom: '1rem' }}>
                          <div style={{ fontSize: '0.72rem', color: '#94a3b8', textTransform: 'uppercase' }}>Emergency Reserve Retained</div>
                          <div style={{ fontSize: '1.2rem', fontWeight: 700, color: opt.emergency_buffer_preserved_pct >= 100 ? '#34d399' : '#fbbf24' }}>
                            {opt.emergency_buffer_preserved_pct.toFixed(0)}%
                          </div>
                        </div>

                        <div style={{ fontSize: '0.78rem', color: '#cbd5e1', borderTop: '1px solid rgba(255,255,255,0.08)', paddingTop: '0.8rem' }}>
                          <b>Trade-off:</b><br />{opt.key_tradeoff}
                        </div>
                      </div>
                    );
                  })}
                </div>
              </div>
            )}

            {/* Installments List */}
            {activeTab === 'installments' && (
              <div>
                <h3 style={{ fontSize: '1.3rem', fontWeight: 800, marginBottom: '1.2rem', color: '#ffffff' }}>
                  📅 Active Installment Commitments & Calendar Reminders
                </h3>
                <div style={{ display: 'flex', flexDirection: 'column', gap: '1.2rem' }}>
                  {installments.map((inst) => (
                    <div key={inst.id} style={{ background: 'linear-gradient(135deg, rgba(18, 27, 46, 0.85) 0%, rgba(10, 16, 28, 0.95) 100%)', borderRadius: '20px', padding: '1.6rem', border: '1px solid rgba(255,255,255,0.08)', borderLeft: '5px solid #06b6d4', display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                      <div>
                        <div style={{ fontWeight: 800, fontSize: '1.3rem', color: '#ffffff' }}>{inst.purchase_name}</div>
                        <div style={{ color: '#94a3b8', fontSize: '0.88rem', marginTop: '0.3rem' }}>
                          EMI: <b style={{ color: '#34d399' }}>₹{inst.monthly_emi.toLocaleString()}/mo</b> | Due Day: <b>{inst.due_day}th of every month</b>
                        </div>
                      </div>
                      <div style={{ textAlign: 'right' }}>
                        <div style={{ fontSize: '1.4rem', fontWeight: 800, color: '#34d399' }}>{inst.paid_installments_count} / {inst.tenure_months} Paid</div>
                        <a
                          href={`http://localhost:8000/api/installments/${inst.id}/calendar`}
                          download
                          style={{ display: 'inline-block', marginTop: '0.6rem', padding: '0.5rem 1rem', background: 'linear-gradient(135deg, #10b981 0%, #059669 100%)', color: '#041a11', borderRadius: '10px', textDecoration: 'none', fontWeight: 800, fontSize: '0.82rem' }}
                        >
                          📅 Download Calendar Reminders (.ics)
                        </a>
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            )}
          </div>
        )}
      </main>
    </div>
  );
}
