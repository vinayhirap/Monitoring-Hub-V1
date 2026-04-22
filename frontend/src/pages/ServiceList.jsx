import { useEffect, useState } from "react";
import { useParams, useNavigate } from "react-router-dom";

const SERVICES = [
  { id:"ec2",    label:"EC2",    icon:"🖥",  desc:"Compute instances",     color:"#00c7ff" },
  { id:"ebs",    label:"EBS",    icon:"💾",  desc:"Block storage volumes",  color:"#38bdf8" },
  { id:"rds",    label:"RDS",    icon:"🗄",  desc:"Managed databases",      color:"#a78bfa" },
  { id:"s3",     label:"S3",     icon:"🪣",  desc:"Object storage buckets", color:"#fbbf24" },
  { id:"ecs",    label:"ECS",    icon:"📦",  desc:"Container services",     color:"#34d399" },
  { id:"elb",    label:"ELB",    icon:"⚖",   desc:"Load balancers",         color:"#f472b6" },
  { id:"lambda", label:"Lambda", icon:"λ",   desc:"Serverless functions",   color:"#00e5a0" },
];

export default function ServiceList() {
  const { id }    = useParams();
  const navigate  = useNavigate();
  const [account, setAccount] = useState(null);

  useEffect(() => {
    fetch(`http://localhost:8000/admin/accounts/${id}`)
      .then(r => r.ok ? r.json() : null)
      .then(d => { if (d) setAccount(d); })
      .catch(console.error);
  }, [id]);

  return (
    <div style={{ maxWidth: 980 }}>
      {/* Breadcrumb */}
      <div style={{ display:"flex", alignItems:"center", gap:6, marginBottom:20, fontSize:11, color:"var(--text-muted)", fontFamily:"var(--font-mono)", letterSpacing:"0.06em" }}>
        <span style={{ cursor:"pointer", color:"var(--accent)", transition:"opacity .15s" }}
              onClick={() => navigate("/overview")}
              onMouseEnter={e=>e.target.style.opacity=".7"}
              onMouseLeave={e=>e.target.style.opacity="1"}>
          ALL ACCOUNTS
        </span>
        <span style={{ opacity:.4 }}>›</span>
        <span style={{ color:"var(--text-secondary)" }}>{account?.account_name ?? `Account ${id}`}</span>
        <span style={{ opacity:.4 }}>›</span>
        <span>SERVICES</span>
      </div>

      {/* Header */}
      <div style={{ marginBottom:28 }}>
        <h1 style={{ fontSize:22, fontWeight:700, marginBottom:5, letterSpacing:"-0.01em" }}>
          {account?.account_name ?? "Account"}
          <span style={{ color:"var(--accent)", marginLeft:8 }}>/ Services</span>
        </h1>
        <p style={{ color:"var(--text-muted)", fontSize:12 }}>
          {account?.account_id} · {account?.default_region} · Select a service to inspect resources
        </p>
      </div>

      {/* Grid */}
      <div style={{ display:"grid", gridTemplateColumns:"repeat(auto-fill,minmax(200px,1fr))", gap:14 }}>
        {SERVICES.map(svc => (
          <ServiceCard key={svc.id} svc={svc} onClick={() => navigate(`/accounts/${id}/${svc.id}`)} />
        ))}
      </div>
    </div>
  );
}

function ServiceCard({ svc, onClick }) {
  const [hovered, setHovered] = useState(false);
  return (
    <div
      onClick={onClick}
      onMouseEnter={() => setHovered(true)}
      onMouseLeave={() => setHovered(false)}
      style={{
        background:    hovered ? "var(--bg-card-hover)" : "var(--bg-card)",
        border:        `1px solid ${hovered ? svc.color + "55" : "var(--border)"}`,
        borderRadius:  "var(--radius-lg)",
        padding:       "22px 18px 18px",
        cursor:        "pointer",
        transition:    "all .18s ease",
        textAlign:     "center",
        position:      "relative",
        overflow:      "hidden",
        transform:     hovered ? "translateY(-3px)" : "translateY(0)",
        boxShadow:     hovered ? `0 8px 24px ${svc.color}18` : "none",
      }}
    >
      {/* top accent bar */}
      <div style={{
        position:"absolute", top:0, left:0, right:0, height:2,
        background:`linear-gradient(90deg,${svc.color}00,${svc.color},${svc.color}00)`,
        opacity: hovered ? 1 : 0.4,
        transition:"opacity .18s",
      }}/>

      {/* glow blob behind icon */}
      <div style={{
        position:"absolute", top:"20%", left:"50%", transform:"translateX(-50%)",
        width:60, height:60, borderRadius:"50%",
        background: svc.color + "18",
        filter:"blur(16px)",
        opacity: hovered ? 1 : 0,
        transition:"opacity .2s",
        pointerEvents:"none",
      }}/>

      <div style={{ fontSize:32, marginBottom:10, position:"relative" }}>{svc.icon}</div>
      <div style={{ fontWeight:700, fontSize:14, color:"var(--text-primary)", marginBottom:5 }}>{svc.label}</div>
      <div style={{ fontSize:11, color:"var(--text-muted)", lineHeight:1.5, marginBottom:12 }}>{svc.desc}</div>
      <div style={{
        fontSize:10, fontFamily:"var(--font-mono)", fontWeight:700,
        color: svc.color, letterSpacing:"0.08em",
        opacity: hovered ? 1 : 0.5,
        transition:"opacity .18s",
      }}>
        OPEN →
      </div>
    </div>
  );
}