import React, { useState, useEffect } from 'react';
import { api } from './lib/api';
import { FinancialProfile } from './types';

export default function App() {
  const [profile, setProfile] = useState<FinancialProfile | null>(null);
  const [activeTab, setActiveTab] = useState<'overview' | 'simulator' | 'purchases' | 'emi' | 'installments' | 'profile'>('overview');
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadProfile();
  }, []);

  const loadProfile = async () => {
    try {
      setLoading(true);
      const data = await api.getProfile();
      setProfile(data);
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={{ display: 'flex', minHeight: '100vh', backgroundColor: '#0a0f1d', color: '#f8fafc', fontFamily: 'sans-serif' }}>
      {/* Sidebar */}
      <div style={{ width: '260px', backgroundColor: '#0d1322', borderRight: '1px solid #1e293b', padding: '1.5rem' }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: '10px', marginBottom: '2rem' }}>
          <span style={{ fontSize: '1.75rem' }}>🌌</span>
          <div>
            <h2 style={{ margin: 0, fontSize: '1.1rem', fontWeight: 700, color: '#10b981' }}>Parallelverse</h2>
            <div style={{ fontSize: '0.75rem', color: '#94a3b8' }}>FinTech Simulator</div>
          </div>
        </div>

        <nav style={{ display: 'flex', flexDirection: 'column', gap: '0.5rem' }}>
          {[
            { id: 'overview', label: '📊 Overview' },
            { id: 'simulator', label: '🔮 Parallel Futures' },
            { id: 'purchases', label: '⚖️ Purchase Planner' },
            { id: 'emi', label: '🧮 EMI Calculator' },
            { id: 'installments', label: '📅 Installments & Reminders' },
            { id: 'profile', label: '👤 Profile' }
          ].map((tab) => (
            <button
              key={tab.id}
              onClick={() => setActiveTab(tab.id as any)}
              style={{
                textAlign: 'left',
                padding: '0.75rem 1rem',
                borderRadius: '8px',
                border: 'none',
                cursor: 'pointer',
                fontWeight: 600,
                fontSize: '0.9rem',
                backgroundColor: activeTab === tab.id ? '#10b981' : 'transparent',
                color: activeTab === tab.id ? '#0a0f1d' : '#94a3b8',
                transition: 'all 0.2s'
              }}
            >
              {tab.label}
            </button>
          ))}
        </nav>

        {profile && (
          <div style={{ marginTop: '3rem', borderTop: '1px solid #1e293b', paddingTop: '1rem', fontSize: '0.8rem', color: '#94a3b8' }}>
            <div>User: <strong style={{ color: '#f8fafc' }}>{profile.full_name}</strong></div>
            <div>Income: ₹{profile.monthly_income.toLocaleString()}</div>
            <div>Savings: ₹{profile.current_savings.toLocaleString()}</div>
          </div>
        )}
      </div>

      {/* Main Content Area */}
      <div style={{ flex: 1, padding: '2rem', overflowY: 'auto' }}>
        {loading ? (
          <div>Loading Financial Parallelverse...</div>
        ) : (
          <div>
            <header style={{ marginBottom: '2rem' }}>
              <h1 style={{ margin: '0 0 0.5rem 0', fontSize: '1.75rem', fontWeight: 700 }}>
                {activeTab === 'overview' && '📊 Executive Financial Overview'}
                {activeTab === 'simulator' && '🔮 Parallel Futures Simulation Engine'}
                {activeTab === 'purchases' && '⚖️ Purchase Affordability Decision Matrix'}
                {activeTab === 'emi' && '🧮 Reducing-Balance EMI Amortization'}
                {activeTab === 'installments' && '📅 Installment Tracker & Calendar Reminders'}
                {activeTab === 'profile' && '👤 Financial Profile Settings'}
              </h1>
              <p style={{ margin: 0, color: '#94a3b8', fontSize: '0.9rem' }}>
                Explore your financial futures before making a major purchase commitment.
              </p>
            </header>

            {/* Content Display */}
            {profile && (
              <div style={{ display: 'grid', gridTemplateColumns: 'repeat(4, 1fr)', gap: '1rem', marginBottom: '2rem' }}>
                <div style={{ backgroundColor: '#131b2e', border: '1px solid #1e293b', borderRadius: '10px', padding: '1.25rem' }}>
                  <div style={{ color: '#94a3b8', fontSize: '0.8rem', textTransform: 'uppercase' }}>Monthly Free Cash Flow</div>
                  <div style={{ fontSize: '1.5rem', fontWeight: 700, color: profile.free_cash_flow < 0 ? '#ef4444' : '#10b981' }}>
                    ₹{profile.free_cash_flow.toLocaleString()}
                  </div>
                </div>
                <div style={{ backgroundColor: '#131b2e', border: '1px solid #1e293b', borderRadius: '10px', padding: '1.25rem' }}>
                  <div style={{ color: '#94a3b8', fontSize: '0.8rem', textTransform: 'uppercase' }}>Liquid Savings</div>
                  <div style={{ fontSize: '1.5rem', fontWeight: 700 }}>₹{profile.current_savings.toLocaleString()}</div>
                </div>
                <div style={{ backgroundColor: '#131b2e', border: '1px solid #1e293b', borderRadius: '10px', padding: '1.25rem' }}>
                  <div style={{ color: '#94a3b8', fontSize: '0.8rem', textTransform: 'uppercase' }}>Emergency Runway</div>
                  <div style={{ fontSize: '1.5rem', fontWeight: 700 }}>{profile.months_of_runway.toFixed(1)} Months</div>
                </div>
                <div style={{ backgroundColor: '#131b2e', border: '1px solid #1e293b', borderRadius: '10px', padding: '1.25rem' }}>
                  <div style={{ color: '#94a3b8', fontSize: '0.8rem', textTransform: 'uppercase' }}>Debt-to-Income</div>
                  <div style={{ fontSize: '1.5rem', fontWeight: 700, color: profile.debt_to_income_pct > 30 ? '#f59e0b' : '#f8fafc' }}>
                    {profile.debt_to_income_pct.toFixed(1)}%
                  </div>
                </div>
              </div>
            )}

            <div style={{ backgroundColor: '#131b2e', border: '1px solid #1e293b', borderRadius: '12px', padding: '1.5rem' }}>
              <div style={{ color: '#10b981', fontWeight: 600, marginBottom: '0.5rem' }}>🚀 Streamlit + FastAPI Unified Experience</div>
              <p style={{ color: '#94a3b8', fontSize: '0.9rem', lineHeight: '1.5' }}>
                For the live college hackathon demonstration, the full interactive user interface is running via Streamlit at 
                <strong style={{ color: '#f8fafc' }}> http://localhost:8501</strong> with live Plotly visualization charts,
                and the FastAPI backend is running at <strong style={{ color: '#f8fafc' }}>http://localhost:8000/api/docs</strong>.
              </p>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
