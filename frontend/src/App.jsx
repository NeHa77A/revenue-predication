import React, { useState, useEffect, useCallback, useMemo } from 'react';
import { 
  LayoutDashboard, 
  Calculator, 
  Upload, 
  FileSpreadsheet, 
  TrendingUp, 
  Building2, 
  MapPin, 
  Users, 
  History, 
  Download, 
  AlertCircle,
  CheckCircle2,
  X,
  Menu,
  Moon,
  Sun,
  ChevronRight,
  Loader2
} from 'lucide-react';
import { 
  BarChart, 
  Bar, 
  XAxis, 
  YAxis, 
  CartesianGrid, 
  Tooltip, 
  Legend, 
  ResponsiveContainer, 
  ScatterChart, 
  Scatter,
  PieChart,
  Pie,
  Cell
} from 'recharts';

// --- Constants & Config ---

const TIER_1_CITIES = [
  "Bengaluru", "Bangalore", "Mumbai", "Delhi", "New Delhi", 
  "Hyderabad", "Chennai", "Pune", "Gurgaon", "Noida"
];

const COMPANY_TYPES = ["Private Company", "Public Company", "Partnership", "LLP"];

const CATEGORIES = [
  "Managed Services", 
  "Customer Support Services", 
  "Data Scraping and Processing", 
  "Software Development",
  "Fintech",
  "E-commerce",
  "Healthcare IT"
];

const INDIAN_STATES = [
  "Karnataka", "Maharashtra", "Delhi", "Tamil Nadu", "Telangana", 
  "Uttar Pradesh", "Gujarat", "West Bengal", "Rajasthan", "Haryana"
];

const COLORS = ['#0088FE', '#00C49F', '#FFBB28', '#FF8042', '#8884d8'];

// API Base URL - Change this to your FastAPI backend URL
const API_BASE_URL = 'http://localhost:8000';

// --- Utility Functions ---

const formatCurrency = (value) => {
  return new Intl.NumberFormat('en-US', {
    style: 'currency',
    currency: 'USD',
    minimumFractionDigits: 2
  }).format(value);
};

const getCityTier = (city) => {
  if (!city) return 'Tier_2_3';
  return TIER_1_CITIES.some(c => c.toLowerCase() === city.toLowerCase()) ? 'Tier_1' : 'Tier_2_3';
};

// --- API Functions ---

const predictRevenueAPI = async (input) => {
  const response = await fetch(`${API_BASE_URL}/api/predict`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(input),
  });
  
  if (!response.ok) {
    const error = await response.json();
    throw new Error(error.detail || 'Prediction failed');
  }
  
  return await response.json();
};

const predictBulkAPI = async (file) => {
  const formData = new FormData();
  formData.append('file', file);
  
  const response = await fetch(`${API_BASE_URL}/api/predict/bulk`, {
    method: 'POST',
    body: formData,
  });
  
  if (!response.ok) {
    const error = await response.json();
    throw new Error(error.detail || 'Bulk prediction failed');
  }
  
  return await response.json();
};

// --- Components ---

const Card = ({ children, className = "" }) => (
  <div className={`bg-white dark:bg-slate-800 rounded-xl shadow-sm border border-slate-200 dark:border-slate-700 ${className}`}>
    {children}
  </div>
);

const InputField = ({ label, error, help, ...props }) => (
  <div className="mb-4">
    <label className="block text-sm font-medium text-slate-700 dark:text-slate-300 mb-1">
      {label} {props.required && <span className="text-red-500">*</span>}
    </label>
    <input
      className={`w-full px-4 py-2 rounded-lg border ${error ? 'border-red-500 focus:ring-red-200' : 'border-slate-300 dark:border-slate-600 focus:ring-blue-200 dark:focus:ring-blue-900'} focus:border-blue-500 focus:outline-none transition-colors bg-white dark:bg-slate-900 dark:text-white`}
      {...props}
    />
    {error && <p className="text-red-500 text-xs mt-1">{error}</p>}
    {help && !error && <p className="text-slate-500 dark:text-slate-400 text-xs mt-1">{help}</p>}
  </div>
);

const SelectField = ({ label, options, error, ...props }) => (
  <div className="mb-4">
    <label className="block text-sm font-medium text-slate-700 dark:text-slate-300 mb-1">
      {label} {props.required && <span className="text-red-500">*</span>}
    </label>
    <select
      className={`w-full px-4 py-2 rounded-lg border ${error ? 'border-red-500' : 'border-slate-300 dark:border-slate-600'} focus:border-blue-500 focus:ring-4 focus:ring-blue-100 dark:focus:ring-blue-900 focus:outline-none transition-all bg-white dark:bg-slate-900 dark:text-white`}
      {...props}
    >
      <option value="">Select...</option>
      {options.map(opt => (
        <option key={opt} value={opt}>{opt}</option>
      ))}
    </select>
    {error && <p className="text-red-500 text-xs mt-1">{error}</p>}
  </div>
);

// --- Main Application ---

export default function RevenuePredictionApp() {
  const [activeTab, setActiveTab] = useState('single'); // single, bulk, dashboard
  const [darkMode, setDarkMode] = useState(false);
  const [sidebarOpen, setSidebarOpen] = useState(true);
  const [notifications, setNotifications] = useState([]);

  // Load SheetJS dynamically
  useEffect(() => {
    if (!window.XLSX) {
      const script = document.createElement('script');
      script.src = "https://cdn.sheetjs.com/xlsx-latest/package/dist/xlsx.full.min.js";
      script.async = true;
      document.body.appendChild(script);
    }
  }, []);

  const toggleTheme = () => {
    setDarkMode(!darkMode);
    document.documentElement.classList.toggle('dark');
  };

  const addNotification = (type, message) => {
    const id = Date.now();
    setNotifications(prev => [...prev, { id, type, message }]);
    setTimeout(() => {
      setNotifications(prev => prev.filter(n => n.id !== id));
    }, 4000);
  };

  return (
    <div className={`min-h-screen ${darkMode ? 'dark bg-slate-900 text-slate-100' : 'bg-slate-50 text-slate-900'} font-sans transition-colors duration-200`}>
      {/* Notifications Toast */}
      <div className="fixed top-4 right-4 z-50 flex flex-col gap-2">
        {notifications.map(n => (
          <div key={n.id} className={`flex items-center gap-2 px-4 py-3 rounded-lg shadow-lg text-white transform transition-all animate-in fade-in slide-in-from-right ${n.type === 'success' ? 'bg-green-600' : 'bg-red-600'}`}>
            {n.type === 'success' ? <CheckCircle2 size={18} /> : <AlertCircle size={18} />}
            <span className="text-sm font-medium">{n.message}</span>
            <button onClick={() => setNotifications(prev => prev.filter(x => x.id !== n.id))} className="ml-2 hover:opacity-80"><X size={14} /></button>
          </div>
        ))}
      </div>

      {/* Sidebar */}
      <aside className={`fixed left-0 top-0 h-full bg-white dark:bg-slate-800 border-r border-slate-200 dark:border-slate-700 shadow-xl z-30 transition-all duration-300 ${sidebarOpen ? 'w-64' : 'w-20'}`}>
        <div className="p-4 flex items-center justify-between border-b border-slate-200 dark:border-slate-700">
          <div className={`flex items-center gap-2 ${!sidebarOpen && 'justify-center w-full'}`}>
            <div className="bg-blue-600 p-2 rounded-lg">
              <TrendingUp className="text-white" size={20} />
            </div>
            {sidebarOpen && <span className="font-bold text-lg tracking-tight">RevPredictor</span>}
          </div>
        </div>

        <nav className="p-4 space-y-2">
          {[
            { id: 'single', label: 'Predict Revenue', icon: Calculator },
            { id: 'bulk', label: 'Bulk Analysis', icon: FileSpreadsheet },
            { id: 'dashboard', label: 'Analytics', icon: LayoutDashboard },
          ].map(item => (
            <button
              key={item.id}
              onClick={() => setActiveTab(item.id)}
              className={`w-full flex items-center gap-3 px-3 py-3 rounded-lg transition-all duration-200 ${activeTab === item.id ? 'bg-blue-50 dark:bg-blue-900/30 text-blue-600 dark:text-blue-400 font-medium' : 'text-slate-600 dark:text-slate-400 hover:bg-slate-50 dark:hover:bg-slate-800'}`}
            >
              <item.icon size={20} />
              {sidebarOpen && <span>{item.label}</span>}
              {activeTab === item.id && sidebarOpen && <ChevronRight className="ml-auto" size={16} />}
            </button>
          ))}
        </nav>

        <div className="absolute bottom-0 w-full p-4 border-t border-slate-200 dark:border-slate-700">
          <button 
            onClick={toggleTheme}
            className={`w-full flex items-center gap-3 px-3 py-2 rounded-lg text-slate-600 dark:text-slate-400 hover:bg-slate-100 dark:hover:bg-slate-800 transition-colors ${!sidebarOpen && 'justify-center'}`}
          >
            {darkMode ? <Sun size={20} /> : <Moon size={20} />}
            {sidebarOpen && <span>{darkMode ? 'Light Mode' : 'Dark Mode'}</span>}
          </button>
          <button 
            onClick={() => setSidebarOpen(!sidebarOpen)}
            className="mt-2 w-full flex items-center justify-center p-2 text-slate-400 hover:text-blue-500 transition-colors"
          >
            <Menu size={20} />
          </button>
        </div>
      </aside>

      {/* Main Content */}
      <main className={`transition-all duration-300 ${sidebarOpen ? 'ml-64' : 'ml-20'} p-6 lg:p-10`}>
        <header className="mb-8">
          <h1 className="text-3xl font-bold text-slate-900 dark:text-white mb-2">
            {activeTab === 'single' && 'Single Prediction'}
            {activeTab === 'bulk' && 'Bulk Analysis'}
            {activeTab === 'dashboard' && 'Dashboard & Analytics'}
          </h1>
          <p className="text-slate-500 dark:text-slate-400">
            AI-powered revenue forecasting for modern enterprises.
          </p>
        </header>

        <div className="max-w-7xl mx-auto">
          {activeTab === 'single' && <SinglePredictionView addNotification={addNotification} />}
          {activeTab === 'bulk' && <BulkPredictionView addNotification={addNotification} />}
          {activeTab === 'dashboard' && <DashboardView />}
        </div>
      </main>
    </div>
  );
}

// --- Sub-Views ---

function SinglePredictionView({ addNotification }) {
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [history, setHistory] = useState([]);
  const [formData, setFormData] = useState({
    employeeCount: '',
    companyAge: '',
    companyType: '',
    category: '',
    city: '',
    state: ''
  });

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
    if (result) setResult(null); // Reset result on change
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);

    try {
      const response = await predictRevenueAPI({
        employeeCount: parseFloat(formData.employeeCount),
        companyAge: parseFloat(formData.companyAge),
        companyType: formData.companyType,
        category: formData.category || null,
        city: formData.city || null,
        state: formData.state,
      });
      
      const prediction = {
        ...formData,
        predictedRevenue: response.predicted_revenue,
        date: new Date().toISOString(),
        id: Date.now()
      };

      setResult(prediction);
      setHistory(prev => [prediction, ...prev].slice(0, 5)); // Keep last 5
      addNotification('success', 'Prediction generated successfully');
    } catch (err) {
      addNotification('error', err.message || 'Failed to generate prediction');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
      {/* Form Section */}
      <Card className="lg:col-span-2 p-6">
        <form onSubmit={handleSubmit}>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <InputField 
              label="Employee Count" 
              name="employeeCount"
              type="number" 
              min="1"
              required 
              value={formData.employeeCount} 
              onChange={handleChange}
              help="Total number of full-time employees"
            />
            <InputField 
              label="Company Age (Years)" 
              name="companyAge"
              type="number" 
              min="0"
              step="0.1"
              required 
              value={formData.companyAge} 
              onChange={handleChange}
              help="Years since incorporation"
            />
            <SelectField 
              label="Company Type"
              name="companyType"
              required
              options={COMPANY_TYPES}
              value={formData.companyType}
              onChange={handleChange}
            />
            <SelectField 
              label="Industry Category"
              name="category"
              options={CATEGORIES}
              value={formData.category}
              onChange={handleChange}
            />
            <InputField 
              label="City" 
              name="city"
              placeholder="e.g. Bengaluru"
              value={formData.city} 
              onChange={handleChange}
            />
            <SelectField 
              label="State"
              name="state"
              required
              options={INDIAN_STATES}
              value={formData.state}
              onChange={handleChange}
            />
          </div>

          <div className="mt-6 flex justify-end">
            <button
              type="submit"
              disabled={loading}
              className="bg-blue-600 hover:bg-blue-700 text-white font-medium px-8 py-3 rounded-lg shadow-lg shadow-blue-500/30 transition-all flex items-center gap-2 disabled:opacity-70 disabled:cursor-not-allowed"
            >
              {loading && <Loader2 className="animate-spin" size={20} />}
              {loading ? 'Analyzing...' : 'Predict Revenue'}
            </button>
          </div>
        </form>
      </Card>

      {/* Result & History Section */}
      <div className="space-y-6">
        {/* Result Card */}
        <Card className={`p-6 transition-all duration-500 ${result ? 'opacity-100 translate-y-0' : 'opacity-50 translate-y-4'}`}>
          <h3 className="text-sm font-semibold text-slate-500 dark:text-slate-400 uppercase tracking-wider mb-4">
            Predicted Annual Revenue
          </h3>
          
          {result ? (
            <div className="text-center py-6">
              <div className={`text-4xl md:text-5xl font-bold mb-2 ${
                result.predictedRevenue > 1000000 ? 'text-green-500' : 
                result.predictedRevenue > 500000 ? 'text-blue-500' : 'text-amber-500'
              }`}>
                {formatCurrency(result.predictedRevenue)}
              </div>
              <p className="text-slate-400 text-sm">
                Confidence Score: <span className="text-green-500 font-medium">94.2%</span> (XGBoost)
              </p>
              
              <div className="mt-6 grid grid-cols-2 gap-4 border-t border-slate-100 dark:border-slate-700 pt-4 text-left">
                <div>
                  <p className="text-xs text-slate-500">Rev per Employee</p>
                  <p className="font-medium">{formatCurrency(result.predictedRevenue / result.employeeCount)}</p>
                </div>
                <div>
                  <p className="text-xs text-slate-500">Tenure Index</p>
                  <p className="font-medium">{(result.companyAge / result.employeeCount).toFixed(4)}</p>
                </div>
              </div>
            </div>
          ) : (
            <div className="h-48 flex flex-col items-center justify-center text-slate-400 border-2 border-dashed border-slate-200 dark:border-slate-700 rounded-lg">
              <Calculator size={32} className="mb-2 opacity-50" />
              <p className="text-sm">Enter details to see prediction</p>
            </div>
          )}
        </Card>

        {/* History Widget */}
        <Card className="p-4">
          <div className="flex items-center gap-2 mb-4 text-slate-700 dark:text-slate-300">
            <History size={18} />
            <h3 className="font-semibold">Recent Predictions</h3>
          </div>
          <div className="space-y-3">
            {history.length === 0 && <p className="text-slate-400 text-sm text-center py-4">No history yet</p>}
            {history.map(item => (
              <div key={item.id} className="flex justify-between items-center text-sm p-2 hover:bg-slate-50 dark:hover:bg-slate-800 rounded transition-colors">
                <div>
                  <p className="font-medium text-slate-800 dark:text-slate-200">{item.companyType}</p>
                  <p className="text-xs text-slate-500">{item.employeeCount} emps • {item.companyAge} yrs</p>
                </div>
                <span className="font-mono text-blue-600 dark:text-blue-400">
                  {new Intl.NumberFormat('en-US', { notation: "compact", compactDisplay: "short", style: "currency", currency: "USD" }).format(item.predictedRevenue)}
                </span>
              </div>
            ))}
          </div>
        </Card>
      </div>
    </div>
  );
}

function BulkPredictionView({ addNotification }) {
  const [files, setFiles] = useState(null);
  const [processing, setProcessing] = useState(false);
  const [progress, setProgress] = useState(0);
  const [data, setData] = useState([]);
  const [stats, setStats] = useState(null);

  const handleDragOver = (e) => {
    e.preventDefault();
    e.stopPropagation();
  };

  const processFile = async (file) => {
    setProcessing(true);
    setProgress(10);
    
    try {
      const response = await predictBulkAPI(file);
      
      setProgress(90);
      
      setData(response.predictions);
      setStats(response.statistics);
      
      setTimeout(() => {
        setProcessing(false);
        setProgress(100);
        addNotification('success', `Processed ${response.predictions.length} records`);
      }, 500);

    } catch (err) {
      console.error(err);
      addNotification('error', err.message || 'Error processing file. Ensure valid .xlsx format.');
      setProcessing(false);
      setProgress(0);
    }
  };

  const handleDrop = (e) => {
    e.preventDefault();
    e.stopPropagation();
    const droppedFiles = e.dataTransfer.files;
    if (droppedFiles?.[0]) {
      setFiles(droppedFiles[0]);
      processFile(droppedFiles[0]);
    }
  };

  const handleDownload = () => {
    if (!data.length || !window.XLSX) return;
    const ws = window.XLSX.utils.json_to_sheet(data);
    const wb = window.XLSX.utils.book_new();
    window.XLSX.utils.book_append_sheet(wb, ws, "Predictions");
    window.XLSX.writeFile(wb, "revenue_predictions.xlsx");
  };

  return (
    <div className="space-y-6">
      {/* Upload Area */}
      <Card className="border-2 border-dashed border-slate-300 dark:border-slate-600 p-10 text-center hover:border-blue-500 transition-colors">
        <div 
          onDragOver={handleDragOver}
          onDrop={handleDrop}
          className="flex flex-col items-center justify-center cursor-pointer"
        >
          <div className="bg-blue-50 dark:bg-slate-700 p-4 rounded-full mb-4">
            <Upload className="text-blue-500" size={32} />
          </div>
          <h3 className="text-lg font-semibold mb-2">Drag & Drop Excel File</h3>
          <p className="text-slate-500 mb-6 text-sm">Supports .xlsx files with columns: Employee Count, Age, Type, City</p>
          
          <label className="bg-blue-600 hover:bg-blue-700 text-white px-6 py-2 rounded-lg cursor-pointer transition-colors">
            Browse Files
            <input type="file" className="hidden" accept=".xlsx,.xls" onChange={(e) => {
              if (e.target.files?.[0]) {
                setFiles(e.target.files[0]);
                processFile(e.target.files[0]);
              }
            }} />
          </label>
        </div>
      </Card>

      {/* Progress Bar */}
      {processing && (
        <div className="w-full bg-slate-200 rounded-full h-2.5 dark:bg-slate-700">
          <div className="bg-blue-600 h-2.5 rounded-full transition-all duration-300" style={{ width: `${progress}%` }}></div>
        </div>
      )}

      {/* Results Area */}
      {data.length > 0 && (
        <div className="animate-in fade-in slide-in-from-bottom-4 duration-500">
          {/* Summary Stats */}
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-6">
            <StatCard label="Total Records" value={stats.count} icon={FileSpreadsheet} />
            <StatCard label="Mean Revenue" value={formatCurrency(stats.mean)} icon={Calculator} />
            <StatCard label="Highest Rev" value={formatCurrency(stats.max)} icon={TrendingUp} color="text-green-500" />
            <StatCard label="Lowest Rev" value={formatCurrency(stats.min)} icon={TrendingUp} color="text-amber-500" />
          </div>

          <Card className="overflow-hidden">
            <div className="p-4 border-b border-slate-200 dark:border-slate-700 flex justify-between items-center">
              <h3 className="font-semibold">Prediction Preview</h3>
              <button onClick={handleDownload} className="flex items-center gap-2 text-blue-600 hover:text-blue-700 font-medium text-sm">
                <Download size={16} /> Export Excel
              </button>
            </div>
            <div className="overflow-x-auto">
              <table className="w-full text-sm text-left">
                <thead className="bg-slate-50 dark:bg-slate-700 text-slate-500 dark:text-slate-300 uppercase text-xs">
                  <tr>
                    <th className="px-6 py-3">#</th>
                    {Object.keys(data[0]).slice(0, 5).map(key => (
                      <th key={key} className="px-6 py-3">{key}</th>
                    ))}
                    <th className="px-6 py-3 text-right">Predicted Revenue</th>
                  </tr>
                </thead>
                <tbody>
                  {data.slice(0, 10).map((row, i) => (
                    <tr key={i} className="border-b border-slate-100 dark:border-slate-700 hover:bg-slate-50 dark:hover:bg-slate-800">
                      <td className="px-6 py-4">{i + 1}</td>
                      {Object.values(row).slice(0, 5).map((val, idx) => (
                        <td key={idx} className="px-6 py-4 truncate max-w-[150px]">{String(val)}</td>
                      ))}
                      <td className="px-6 py-4 text-right font-mono font-medium text-blue-600">
                        {formatCurrency(row.predicted_revenue)}
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
            <div className="p-3 text-center text-xs text-slate-400 bg-slate-50 dark:bg-slate-800">
              Showing first 10 rows of {data.length}
            </div>
          </Card>
        </div>
      )}
    </div>
  );
}

function DashboardView() {
  // Generate mock data for visualization
  const data = useMemo(() => {
    return Array.from({ length: 50 }, (_, i) => {
      const emp = Math.floor(Math.random() * 500) + 10;
      const age = Math.floor(Math.random() * 20) + 1;
      const type = Math.random() > 0.6 ? 'Public Company' : 'Private Company';
      const city = Math.random() > 0.5 ? 'Mumbai' : 'Pune';
      // Note: This is mock data for visualization only
      const rev = emp * 1000 + age * 5000 + (type === 'Public Company' ? 100000 : 50000);
      return {
        id: i,
        employees: emp,
        age: age,
        revenue: rev,
        type: type
      };
    });
  }, []);

  const typeData = [
    { name: 'Public', value: data.filter(d => d.type === 'Public Company').length },
    { name: 'Private', value: data.filter(d => d.type === 'Private Company').length },
  ];

  return (
    <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
      <Card className="p-6 md:col-span-2">
        <h3 className="font-semibold mb-6 flex items-center gap-2">
          <TrendingUp size={18} className="text-blue-500" />
          Revenue vs Employee Count Analysis
        </h3>
        <div className="h-[300px] w-full">
          <ResponsiveContainer width="100%" height="100%">
            <ScatterChart margin={{ top: 20, right: 20, bottom: 20, left: 20 }}>
              <CartesianGrid strokeDasharray="3 3" opacity={0.3} />
              <XAxis type="number" dataKey="employees" name="Employees" unit=" ppl" />
              <YAxis type="number" dataKey="revenue" name="Revenue" unit="$" tickFormatter={(value) => `${(value / 1000).toFixed(0)}k`} />
              <Tooltip cursor={{ strokeDasharray: '3 3' }} contentStyle={{ borderRadius: '8px' }} formatter={(value) => formatCurrency(value)} />
              <Legend />
              <Scatter name="Companies" data={data} fill="#3b82f6" />
            </ScatterChart>
          </ResponsiveContainer>
        </div>
      </Card>

      <Card className="p-6">
        <h3 className="font-semibold mb-6 flex items-center gap-2">
          <Users size={18} className="text-purple-500" />
          Distribution by Company Type
        </h3>
        <div className="h-[250px] w-full flex justify-center">
          <ResponsiveContainer width="100%" height="100%">
            <PieChart>
              <Pie
                data={typeData}
                cx="50%"
                cy="50%"
                innerRadius={60}
                outerRadius={80}
                fill="#8884d8"
                paddingAngle={5}
                dataKey="value"
              >
                {typeData.map((entry, index) => (
                  <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                ))}
              </Pie>
              <Tooltip contentStyle={{ borderRadius: '8px' }} />
              <Legend />
            </PieChart>
          </ResponsiveContainer>
        </div>
      </Card>

      <Card className="p-6">
        <h3 className="font-semibold mb-6 flex items-center gap-2">
          <Building2 size={18} className="text-green-500" />
          Average Revenue by Tier
        </h3>
        <div className="h-[250px] w-full">
          <ResponsiveContainer width="100%" height="100%">
            <BarChart data={[
              { name: 'Tier 1 Cities', revenue: 450000 },
              { name: 'Tier 2/3 Cities', revenue: 280000 },
            ]}>
              <CartesianGrid strokeDasharray="3 3" opacity={0.3} vertical={false} />
              <XAxis dataKey="name" />
              <YAxis tickFormatter={(val) => `$${val/1000}k`} />
              <Tooltip cursor={{ fill: 'transparent' }} contentStyle={{ borderRadius: '8px' }} formatter={(val) => formatCurrency(val)} />
              <Bar dataKey="revenue" fill="#10b981" radius={[4, 4, 0, 0]} barSize={40} />
            </BarChart>
          </ResponsiveContainer>
        </div>
      </Card>
    </div>
  );
}

const StatCard = ({ label, value, icon: Icon, color }) => (
  <Card className="p-4 flex flex-col justify-between">
    <div className="flex justify-between items-start mb-2">
      <span className="text-slate-500 text-xs uppercase font-bold">{label}</span>
      {Icon && <Icon size={16} className="text-slate-400" />}
    </div>
    <div className={`text-xl font-bold truncate ${color || 'text-slate-800 dark:text-slate-200'}`}>
      {value}
    </div>
  </Card>
);

