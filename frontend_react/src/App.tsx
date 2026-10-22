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

      // Pre-run baseline simulation
      const sim = await api.simulateScenarios({
        duration_months: 12,
        purchase_name: prof.planned_purchase_name,
        purchase_amount: prof.planned_purchase_amount,
        purchase_mode: 'EMI'
      });
      setSimResults(sim);

      // Pre-run purchase evaluation
      const purch = await api.evaluatePurchase({
        purchase_name: prof.planned_purchase_name,
        purchase_amount: prof.planned_purchase_amount,
        cheaper_alternative_amount: 42000,
        wait_months: 4
      });
      setPurchaseResults(purch);

      // Load installments
      const inst = await api.getInstallments();
      setInstallments(inst);
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={{ display: 'flex', minHeight: '100vh', backgroundColor: '#070b14', color: '#f8fafc', fontFamily: 'system-ui, -apple-system, sans-serif' }}>
      {/* Sidebar */}
      <aside style={{ width: '280px', backgroundColor: '#0c111e', borderRight: '1px solid rgba(255,255,255,0.08)', padding: '1.75rem 1.25rem', display: 'flex', flexDirection: 'column' }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: '12px', marginBottom: '2.5rem' }}>
          <div style={{ width: '42px', height: '42px', borderRadius: '12px', background: 'linear-gradient(135deg, #10b981 0%, #06b6d4 100%)', display: 'flex', alignItems: 'center', justifyContent: 'center', fontSize: '1.5rem', boxShadow: '0 4px 14px rgba(16, 185, 129, 0.35)' }}>
            🌌
          </div>
          <div>
            <h2 style={{ margin: 0, fontSize: '1.2rem', fontWeight: 800, color: '#f8fafc', letterSpacing: '-0.02em' }}>Parallelverse</h2>
            <div style={{ fontSize: '0.75rem', color: '#10b981', fontWeight: 600 }}>FinTech Simulator</div>
          </div>
        </div>

        <nav style={{ display: 'flex', flexDirection: 'column', gap: '0.5rem', flex: 1 }}>
          {[
            { id: 'overview', label: '📊 Executive Overview' },
            { id: 'simulator', label: '🔮 Parallel Futures' },
            { id: 'purchases', label: '⚖️ Purchase Matrix' },
            { id: 'emi', label: '🧮 EMI Calculator' },
            { id: 'installments', label: '📅 Installment Tracker' },
            { id: 'profile', label: '👤 Financial Profile' }
          ].map((tab) => {
            const isActive = activeTab === tab.id;
            return (
              <button
                key={tab.id}
                onClick={() => setActiveTab(tab.id as any)}
                style={{
                  textAlign: 'left',
                  padding: '0.85rem 1.15rem',
                  borderRadius: '10px',
                  border: 'none',
                  cursor: 'pointer',
                  fontWeight: 600,
                  fontSize: '0.9rem',
                  backgroundColor: isActive ? 'rgba(16, 185, 129, 0.15)' : 'transparent',
                  color: isActive ? '#10b981' : '#94a3b8',
                  borderLeft: isActive ? '3px solid #10b981' : '3px solid transparent',
                  transition: 'all 0.2s ease'
                }}
              >
                {tab.label}
              </button>
            );
          })}
        </nav>

        {profile && (
          <div style={{ backgroundColor: 'rgba(255,255,255,0.03)', border: '1px solid rgba(255,255,255,0.06)', borderRadius: '12px', padding: '1rem', fontSize: '0.82rem' }}>
            <div style={{ color: '#94a3b8', fontSize: '0.72rem', textTransform: 'uppercase' }}>Active User</div>
            <div style={{ color: '#f8fafc', fontWeight: 700, fontSize: '0.95rem', margin: '0.2rem 0 0.5rem 0' }}>{profile.full_name}</div>
            <div style={{ display: 'flex', justifyContent: 'space-between', color: '#94a3b8' }}>
              <span>Monthly Inflow:</span>
              <strong style={{ color: '#f8fafc' }}>₹{profile.monthly_income.toLocaleString()}</strong>
            </div>
            <div style={{ display: 'flex', justifyContent: 'space-between', color: '#94a3b8', marginTop: '0.25rem' }}>
              <span>Liquid Savings:</span>
              <strong style={{ color: '#10b981' }}>₹{profile.current_savings.toLocaleString()}</strong>
            </div>
          </div>
        )}
      </aside>

      {/* Main Content Area */}
      <main style={{ flex: 1, padding: '2.5rem', overflowY: 'auto', background: 'radial-gradient(circle at 10% 10%, #0d1527 0%, #080c16 60%, #050811 100%)' }}>
        {loading ? (
          <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'center', height: '100%', color: '#94a3b8' }}>
            Loading Financial Parallelverse...
          </div>
        ) : (
          <div>
            {/* Header */}
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', marginBottom: '2rem' }}>
              <div>
                <h1 style={{ margin: 0, fontSize: '2rem', fontWeight: 800, letterSpacing: '-0.02em', background: 'linear-gradient(135deg, #ffffff 30%, #10b981 100%)', WebkitBackgroundClip: 'text', WebkitTextFillColor: 'transparent' }}>
                  {activeTab === 'overview' && 'Executive Financial Overview'}
                  {activeTab === 'simulator' && 'Parallel Financial Futures Simulation'}
                  {activeTab === 'purchases' && 'Purchase Affordability Decision Matrix'}
                  {activeTab === 'emi' && 'Precision Reducing-Balance EMI Engine'}
                  {activeTab === 'installments' && 'Installment Tracker & Reminders'}
                  {activeTab === 'profile' && 'Financial Profile Settings'}
                </h1>
                <p style={{ margin: '0.4rem 0 0 0', color: '#94a3b8', fontSize: '0.92rem' }}>
                  Simulating multiple possible financial futures before committing to large purchases or installment debt.
                </p>
              </div>

              <div style={{ display: 'flex', gap: '10px' }}>
                <span style={{ display: 'inline-flex', alignItems: 'center', gap: '6px', padding: '0.35rem 0.8rem', borderRadius: '9999px', fontSize: '0.75rem', fontWeight: 700, backgroundColor: 'rgba(16,185,129,0.12)', color: '#34d399', border: '1px solid rgba(16,185,129,0.3)' }}>
                  ● FASTAPI LIVE (:8000)
                </span>
                <span style={{ display: 'inline-flex', alignItems: 'center', gap: '6px', padding: '0.35rem 0.8rem', borderRadius: '9999px', fontSize: '0.75rem', fontWeight: 700, backgroundColor: 'rgba(6,182,212,0.12)', color: '#38bdf8', border: '1px solid rgba(6,182,212,0.3)' }}>
                  STREAMLIT ACTIVE (:8501)
                </span>
              </div>
            </div>

            {/* Stat Row */}
            {profile && (
              <div style={{ display: 'grid', gridTemplateColumns: 'repeat(4, 1fr)', gap: '1.25rem', marginBottom: '2rem' }}>
                <div style={{ background: 'linear-gradient(135deg, rgba(19, 29, 49, 0.7) 0%, rgba(13, 20, 36, 0.85) 100%)', border: '1px solid rgba(255,255,255,0.08)', borderRadius: '16px', padding: '1.4rem' }}>
                  <div style={{ color: '#94a3b8', fontSize: '0.78rem', fontWeight: 600, textTransform: 'uppercase' }}>Monthly Free Cash Flow</div>
                  <div style={{ fontSize: '1.95rem', fontWeight: 800, color: profile.free_cash_flow < 0 ? '#f43f5e' : '#10b981', marginTop: '0.2rem' }}>
                    ₹{profile.free_cash_flow.toLocaleString()}
                  </div>
                  <div style={{ fontSize: '0.78rem', color: '#38bdf8', marginTop: '0.4rem' }}>Savings Rate: {profile.savings_rate_pct.toFixed(1)}%</div>
                </div>

                <div style={{ background: 'linear-gradient(135deg, rgba(19, 29, 49, 0.7) 0%, rgba(13, 20, 36, 0.85) 100%)', border: '1px solid rgba(255,255,255,0.08)', borderRadius: '16px', padding: '1.4rem' }}>
                  <div style={{ color: '#94a3b8', fontSize: '0.78rem', fontWeight: 600, textTransform: 'uppercase' }}>Liquid Reserves</div>
                  <div style={{ fontSize: '1.95rem', fontWeight: 800, marginTop: '0.2rem' }}>₹{profile.current_savings.toLocaleString()}</div>
                  <div style={{ fontSize: '0.78rem', color: '#10b981', marginTop: '0.4rem' }}>Target: ₹{profile.emergency_fund_target.toLocaleString()}</div>
                </div>

                <div style={{ background: 'linear-gradient(135deg, rgba(19, 29, 49, 0.7) 0%, rgba(13, 20, 36, 0.85) 100%)', border: '1px solid rgba(255,255,255,0.08)', borderRadius: '16px', padding: '1.4rem' }}>
                  <div style={{ color: '#94a3b8', fontSize: '0.78rem', fontWeight: 600, textTransform: 'uppercase' }}>Emergency Runway</div>
                  <div style={{ fontSize: '1.95rem', fontWeight: 800, marginTop: '0.2rem' }}>{profile.months_of_runway.toFixed(1)} <span style="font-size: 1rem; color: #94a3b8;">Months</span></div>
                  <div style={{ fontSize: '0.78rem', color: '#38bdf8', marginTop: '0.4rem' }}>Survival without income</div>
                </div>

                <div style={{ background: 'linear-gradient(135deg, rgba(19, 29, 49, 0.7) 0%, rgba(13, 20, 36, 0.85) 100%)', border: '1px solid rgba(255,255,255,0.08)', borderRadius: '16px', padding: '1.4rem' }}>
                  <div style={{ color: '#94a3b8', fontSize: '0.78rem', fontWeight: 600, textTransform: 'uppercase' }}>Debt-to-Income (DTI)</div>
                  <div style={{ fontSize: '1.95rem', fontWeight: 800, color: profile.debt_to_income_pct > 35 ? '#f43f5e' : '#f8fafc', marginTop: '0.2rem' }}>
                    {profile.debt_to_income_pct.toFixed(1)}%
                  </div>
                  <div style={{ fontSize: '0.78rem', color: '#10b981', marginTop: '0.4rem' }}>Safe: &lt; 35%</div>
                </div>
              </div>
            )}

            {/* Tab Specific Content */}
            {activeTab === 'overview' && (
              <div style={{ display: 'grid', gridTemplateColumns: '1.5fr 1fr', gap: '1.5rem' }}>
                <div style={{ background: 'linear-gradient(135deg, rgba(19, 29, 49, 0.7) 0%, rgba(13, 20, 36, 0.85) 100%)', border: '1px solid rgba(255,255,255,0.08)', borderRadius: '16px', padding: '1.75rem' }}>
                  <h3 style={{ margin: '0 0 1rem 0', fontSize: '1.2rem', fontWeight: 700 }}>5 Parallel Futures Resilience Status</h3>
                  {simResults && (
                    <div>
                      <div style={{ padding: '1rem', backgroundColor: 'rgba(16,185,129,0.1)', border: '1px solid rgba(16,185,129,0.3)', borderRadius: '10px', marginBottom: '1.5rem', color: '#d1fae5', fontSize: '0.9rem' }}>
                        💡 <b>Recommendation Verdict:</b> {simResults.recommendation}
                      </div>

                      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(3, 1fr)', gap: '1rem' }}>
                        {Object.entries(simResults.scenarios).slice(0, 3).map(([key, sc]) => (
                          <div key={key} style={{ backgroundColor: 'rgba(255,255,255,0.03)', border: '1px solid rgba(255,255,255,0.06)', borderRadius: '10px', padding: '1rem' }}>
                            <div style={{ fontSize: '0.85rem', fontWeight: 700 }}>{sc.scenario_name}</div>
                            <div style={{ fontSize: '1.25rem', fontWeight: 800, color: sc.lowest_savings < 0 ? '#f43f5e' : '#f8fafc', margin: '0.4rem 0' }}>
                              ₹{sc.lowest_savings.toLocaleString()}
                            </div>
                            <div style={{ fontSize: '0.75rem', color: '#94a3b8' }}>Score: {sc.resilience_score}/100</div>
                          </div>
                        ))}
                      </div>
                    </div>
                  )}
                </div>

                <div style={{ background: 'linear-gradient(135deg, rgba(19, 29, 49, 0.7) 0%, rgba(13, 20, 36, 0.85) 100%)', border: '1px solid rgba(255,255,255,0.08)', borderRadius: '16px', padding: '1.75rem' }}>
                  <h3 style={{ margin: '0 0 1rem 0', fontSize: '1.2rem', fontWeight: 700 }}>Planned Purchase Decision</h3>
                  {profile && (
                    <div>
                      <div style={{ fontSize: '1.4rem', fontWeight: 800, color: '#06b6d4' }}>{profile.planned_purchase_name}</div>
                      <div style={{ fontSize: '2rem', fontWeight: 800, margin: '0.3rem 0 1rem 0' }}>₹{profile.planned_purchase_amount.toLocaleString()}</div>
                      <p style={{ color: '#94a3b8', fontSize: '0.85rem', lineHeight: '1.5' }}>
                        Use the <b>Parallel Futures Simulator</b> or <b>Purchase Matrix</b> to stress test this decision against unexpected emergencies and salary delays.
                      </p>
                    </div>
                  )}
                </div>
              </div>
            )}

            {activeTab === 'simulator' && simResults && (
              <div style={{ background: 'linear-gradient(135deg, rgba(19, 29, 49, 0.7) 0%, rgba(13, 20, 36, 0.85) 100%)', border: '1px solid rgba(255,255,255,0.08)', borderRadius: '16px', padding: '1.75rem' }}>
                <h3 style={{ margin: '0 0 1.25rem 0', fontSize: '1.2rem', fontWeight: 700 }}>All 5 Simulated Parallel Timelines</h3>
                <div style={{ display: 'grid', gridTemplateColumns: 'repeat(5, 1fr)', gap: '1rem' }}>
                  {Object.entries(simResults.scenarios).map(([key, sc]) => (
                    <div key={key} style={{ backgroundColor: 'rgba(255,255,255,0.03)', border: '1px solid rgba(255,255,255,0.08)', borderRadius: '12px', padding: '1.25rem' }}>
                      <div style={{ fontWeight: 700, fontSize: '0.95rem' }}>{sc.scenario_name}</div>
                      <div style={{ marginTop: '0.5rem', display: 'inline-block', padding: '0.2rem 0.6rem', borderRadius: '999px', fontSize: '0.7rem', fontWeight: 700, backgroundColor: sc.risk_level === 'LOW' ? 'rgba(16,185,129,0.2)' : 'rgba(244,63,94,0.2)', color: sc.risk_level === 'LOW' ? '#34d399' : '#fb7185' }}>
                        {sc.risk_level} RISK
                      </div>
                      <div style={{ marginTop: '1rem', fontSize: '0.75rem', color: '#94a3b8' }}>Lowest Point:</div>
                      <div style={{ fontSize: '1.3rem', fontWeight: 800, color: sc.lowest_savings < 0 ? '#f43f5e' : '#f8fafc' }}>
                        ₹{sc.lowest_savings.toLocaleString()}
                      </div>
                      <div style={{ marginTop: '0.8rem', fontSize: '0.75rem', color: '#cbd5e1', borderTop: '1px solid rgba(255,255,255,0.06)', paddingTop: '0.6rem' }}>
                        {sc.breaking_point_reason}
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            )}

            {activeTab === 'purchases' && purchaseResults && (
              <div>
                <div style={{ display: 'grid', gridTemplateColumns: 'repeat(4, 1fr)', gap: '1.25rem' }}>
                  {purchaseResults.options.map((opt) => (
                    <div key={opt.option_id} style={{ background: 'linear-gradient(135deg, rgba(19, 29, 49, 0.7) 0%, rgba(13, 20, 36, 0.85) 100%)', border: opt.option_id === purchaseResults.recommended_option_id ? '2px solid #10b981' : '1px solid rgba(255,255,255,0.08)', borderRadius: '16px', padding: '1.4rem' }}>
                      {opt.option_id === purchaseResults.recommended_option_id && (
                        <div style={{ color: '#10b981', fontSize: '0.75rem', fontWeight: 800, marginBottom: '0.4rem' }}>⭐ RECOMMENDED</div>
                      )}
                      <div style={{ fontWeight: 700, fontSize: '1.05rem' }}>{opt.option_title}</div>
                      <div style={{ margin: '1rem 0 0.5rem 0', fontSize: '0.75rem', color: '#94a3b8' }}>Upfront Cash:</div>
                      <div style={{ fontSize: '1.3rem', fontWeight: 800 }}>₹{opt.upfront_cash_required.toLocaleString()}</div>
                      <div style={{ margin: '0.5rem 0 0 0', fontSize: '0.75rem', color: '#94a3b8' }}>Monthly Drag:</div>
                      <div style={{ fontSize: '1.3rem', fontWeight: 800, color: '#06b6d4' }}>₹{opt.monthly_obligation.toLocaleString()}/mo</div>
                      <div style={{ marginTop: '1rem', borderTop: '1px solid rgba(255,255,255,0.08)', paddingTop: '0.8rem', fontSize: '0.75rem', color: '#94a3b8' }}>
                        {opt.key_tradeoff}
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            )}

            {activeTab === 'installments' && (
              <div style={{ background: 'linear-gradient(135deg, rgba(19, 29, 49, 0.7) 0%, rgba(13, 20, 36, 0.85) 100%)', border: '1px solid rgba(255,255,255,0.08)', borderRadius: '16px', padding: '1.75rem' }}>
                <h3 style={{ margin: '0 0 1.25rem 0', fontSize: '1.2rem', fontWeight: 700 }}>Active Installment Commitments</h3>
                <div style={{ display: 'flex', flexDirection: 'column', gap: '1rem' }}>
                  {installments.map((inst) => (
                    <div key={inst.id} style={{ backgroundColor: 'rgba(255,255,255,0.03)', border: '1px solid rgba(255,255,255,0.08)', borderRadius: '12px', padding: '1.25rem', display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                      <div>
                        <div style={{ fontWeight: 700, fontSize: '1.1rem' }}>{inst.purchase_name}</div>
                        <div style={{ color: '#94a3b8', fontSize: '0.82rem', marginTop: '0.2rem' }}>
                          EMI: <b style={{ color: '#10b981' }}>₹{inst.monthly_emi.toLocaleString()}/mo</b> | Due Day: {inst.due_day}th
                        </div>
                      </div>
                      <div style={{ textAlign: 'right' }}>
                        <div style={{ fontSize: '1.1rem', fontWeight: 700, color: '#10b981' }}>{inst.paid_installments_count} / {inst.tenure_months} Paid</div>
                        <a
                          href={`http://localhost:8000/api/installments/${inst.id}/calendar`}
                          download
                          style={{ display: 'inline-block', marginTop: '0.5rem', padding: '0.4rem 0.8rem', backgroundColor: '#10b981', color: '#041a11', borderRadius: '8px', textDecoration: 'none', fontWeight: 700, fontSize: '0.78rem' }}
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
