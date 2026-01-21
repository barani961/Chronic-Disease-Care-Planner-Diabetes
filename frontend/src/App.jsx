import React, { useState, createContext, useContext,useEffect } from 'react';
import { Home, Settings, FileText, Activity, Calendar, Bell, User, LogOut, ChevronRight, Plus, Info } from 'lucide-react';

// List of countries
const COUNTRIES = [
   'India', 'Indonesia', 'Iran', 'Iraq', 'Ireland', 'Israel',
  'Italy', 'Jamaica', 'Japan', 'Jordan'
].sort();

// ==================== CONTEXT & STATE ====================
const AppContext = createContext();

const useApp = () => {
  const context = useContext(AppContext);
  if (!context) throw new Error('useApp must be used within AppProvider');
  return context;
};

// Mock initial state structure (API-ready)
const initialState = {
  user: {
    username: 'john.doe',
    age: 45,
    condition: 'both',
    region: 'United States',
    isAuthenticated: false
  },
  lastTestResult: {
    fastingSugar: 0,
    postMealSugar: 0,
    date: '2026-01-05'
  },
  selectedDay: new Date().getDay(), // 0 = Sunday, 1 = Monday, etc.
  dietPlan: {
    sunday: {
      day: 'Light breakfast with whole grains, seasonal fruits',
      afternoon: 'Balanced lunch with vegetables, lean protein',
      night: 'Light dinner before 8 PM, avoid heavy carbs',
      lifestyle: 'Stay hydrated, light activity'
    },
    monday: {
      day: 'Oatmeal with fruits and nuts',
      afternoon: 'Grilled chicken salad with veggies',
      night: 'Fish with steamed vegetables',
      lifestyle: 'Maintain consistent meal timings'
    },
    tuesday: {
      day: 'Whole grain toast with avocado',
      afternoon: 'Lentil soup with brown rice',
      night: 'Tofu stir-fry with mixed greens',
      lifestyle: 'Monitor blood sugar levels'
    },
    wednesday: {
      day: 'Greek yogurt with berries',
      afternoon: 'Turkey wrap with lettuce and tomato',
      night: 'Baked salmon with quinoa',
      lifestyle: 'Engage in light exercise'
    },
    thursday: {
      day: 'Smoothie with spinach and banana',
      afternoon: 'Chickpea curry with whole grains',
      night: 'Grilled vegetables with lean protein',
      lifestyle: 'Stay hydrated throughout the day'
    },
    friday: {
      day: 'Eggs with whole grain toast',
      afternoon: 'Vegetable stir-fry with tofu',
      night: 'Light soup and salad',
      lifestyle: 'Avoid heavy carbs in evening'
    },
    saturday: {
      day: 'Fruit salad with yogurt',
      afternoon: 'Quinoa bowl with veggies',
      night: 'Herbal tea and light snacks',
      lifestyle: 'Rest and recover'
    }
  },
  todayActivity: {
    day: { food: false, medicine: false, exercise: false },
    afternoon: { food: false, medicine: false},
    night: { food: false, medicine: false }
  },
  medicationPlan: {
    day: 1,
    afternoon: 0,
    night: 1
  }
};

// ==================== APP PROVIDER ====================
const AppProvider = ({ children }) => {
  const [state, setState] = useState(initialState);
  const [currentPage, setCurrentPage] = useState('login');

  const login = (username, password) => {
    setState(prev => ({
      ...prev,
      user: { ...prev.user, username, isAuthenticated: true }
    }));
    setCurrentPage('dashboard');
  };

  const logout = () => {
    setState(prev => ({
      ...prev,
      user: { ...prev.user, isAuthenticated: false }
    }));
    setCurrentPage('login');
  };

  const updateSettings = (updates) => {
    setState(prev => ({
      ...prev,
      user: { ...prev.user, ...updates }
    }));
  };

  const updateTestResult = (fastingSugar, postMealSugar) => {
    setState(prev => ({
      ...prev,
      lastTestResult: {
        fastingSugar,
        postMealSugar,
        date: new Date().toISOString().split('T')[0]
      }
    }));
  };

  const updateTodayActivity = (time, type, value) => {
    setState(prev => ({
      ...prev,
      todayActivity: {
        ...prev.todayActivity,
        [time]: { ...prev.todayActivity[time], [type]: value }
      }
    }));
  };

  const updateMedicationPlan = (plan) => {
    setState(prev => ({ ...prev, medicationPlan: plan }));
  };

  const selectDay = (dayIndex) => {
    setState(prev => ({ ...prev, selectedDay: dayIndex }));
  };

  return (
    <AppContext.Provider value={{
      state,
      currentPage,
      setCurrentPage,
      login,
      logout,
      updateSettings,
      updateTestResult,
      updateTodayActivity,
      updateMedicationPlan,
      selectDay
    }}>
      {children}
    </AppContext.Provider>
  );
};

// ==================== SHARED COMPONENTS ====================
const Card = ({ children, className = '' }) => (
  <div className={`bg-white rounded-lg shadow-sm p-6 ${className}`}>
    {children}
  </div>
);

const Button = ({ children, onClick, variant = 'primary', className = '', ...props }) => {
  const baseStyles = 'px-6 py-3 rounded-lg font-medium transition-colors min-h-[44px] flex items-center justify-center gap-2';
  const variants = {
    primary: 'bg-teal-600 text-white hover:bg-teal-700',
    secondary: 'bg-gray-100 text-gray-700 hover:bg-gray-200',
    ghost: 'bg-transparent text-teal-600 hover:bg-teal-50'
  };
  
  return (
    <button 
      className={`${baseStyles} ${variants[variant]} ${className}`}
      onClick={onClick}
      {...props}
    >
      {children}
    </button>
  );
};

const Input = ({ label, type = 'text', value, onChange, placeholder, required, ...props }) => (
  <div className="mb-4">
    <label className="block text-sm font-medium text-gray-700 mb-2">
      {label} {required && <span className="text-red-500">*</span>}
    </label>
    <input
      type={type}
      value={value}
      onChange={onChange}
      placeholder={placeholder}
      className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-teal-500 min-h-[44px]"
      {...props}
    />
  </div>
);

const Disclaimer = ({ text }) => (
  <div className="flex items-start gap-2 p-4 bg-blue-50 border border-blue-100 rounded-lg text-sm text-gray-700">
    <Info className="w-4 h-4 text-blue-600 flex-shrink-0 mt-0.5" />
    <p>{text}</p>
  </div>
);

const StatusBadge = ({ status }) => {
  const styles = {
    neutral: 'bg-gray-100 text-gray-700',
    warning: 'bg-amber-50 text-amber-700',
    critical: 'bg-red-50 text-red-700'
  };
  
  return (
    <span className={`px-3 py-1 rounded-full text-xs font-medium ${styles[status]}`}>
      {status.charAt(0).toUpperCase() + status.slice(1)}
    </span>
  );
};

// ==================== LOGIN PAGE ====================
const LoginPage = () => {
  const { login } = useApp();
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');

  const handleSubmit = () => {
    if (username && password) {
      login(username, password);
    }
  };

  return (
    <div className="min-h-screen bg-gray-50 flex items-center justify-center p-4">
      <Card className="w-full max-w-md">
        <div className="text-center mb-8">
          <div className="w-16 h-16 bg-teal-600 rounded-lg mx-auto mb-4 flex items-center justify-center">
            <Activity className="w-8 h-8 text-white" />
          </div>
          <h1 className="text-2xl font-semibold text-gray-900">Care Planner</h1>
          <p className="text-gray-600 mt-2">Chronic Disease Management</p>
        </div>
        
        <div>
          <Input
            label="Username"
            value={username}
            onChange={(e) => setUsername(e.target.value)}
            required
          />
          <Input
            label="Password"
            type="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            required
          />
          
          <a href="#" className="text-sm text-teal-600 hover:text-teal-700 block mb-6">
            Forgot password?
          </a>
          
          <Button onClick={handleSubmit} className="w-full">
            Sign In
          </Button>
        </div>
      </Card>
    </div>
  );
};

// ==================== DASHBOARD PAGE ====================
const DashboardPage = () => {
  const { state, setCurrentPage } = useApp();

  const getTestStatus = (value, type) => {
    if (type === 'fasting') {
      if (value < 100) return 'neutral';
      if (value < 126) return 'warning';
      return 'critical';
    } else {
      if (value < 140) return 'neutral';
      if (value < 200) return 'warning';
      return 'critical';
    }
  };

  const fastingStatus = getTestStatus(state.lastTestResult.fastingSugar, 'fasting');
  const postMealStatus = getTestStatus(state.lastTestResult.postMealSugar, 'postmeal');

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl font-semibold text-gray-900">Dashboard</h1>
        <p className="text-gray-600 mt-1">Welcome back, {state.user.username}</p>
      </div>

     
      {/* Last Test Result */}
      <div>
        <h2 className="text-lg font-medium text-gray-900 mb-4">Last Test Result</h2>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <Card>
            <div className="flex items-start justify-between mb-2">
              <h3 className="text-sm font-medium text-gray-700">Fasting Sugar</h3>
              <StatusBadge status={fastingStatus} />
            </div>
            <p className="text-3xl font-semibold text-gray-900 mb-1">
              {state.lastTestResult.fastingSugar} <span className="text-lg text-gray-600">mg/dL</span>
            </p>
            <p className="text-xs text-gray-500">Last updated: {state.lastTestResult.date}</p>
            <p className="text-xs text-gray-500 mt-2">Values are informational only</p>
          </Card>
          
          <Card>
            <div className="flex items-start justify-between mb-2">
              <h3 className="text-sm font-medium text-gray-700">Post-Meal Sugar</h3>
              <StatusBadge status={postMealStatus} />
            </div>
            <p className="text-3xl font-semibold text-gray-900 mb-1">
              {state.lastTestResult.postMealSugar} <span className="text-lg text-gray-600">mg/dL</span>
            </p>
            <p className="text-xs text-gray-500">Last updated: {state.lastTestResult.date}</p>
            <p className="text-xs text-gray-500 mt-2">Values are informational only</p>
          </Card>
        </div>
      </div>

      {/* Current Diet Plan */}
      <Card>
        <div className="flex items-start justify-between mb-6">
          <div>
            <h2 className="text-lg font-medium text-gray-900">Current Diet Plan</h2>
            <p className="text-sm text-gray-600 mt-1">
              {(() => {
                const dayNames = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday'];
                return dayNames[new Date().getDay()] + "'s Plan";
              })()}
            </p>
          </div>
          <Button variant="ghost" onClick={() => setCurrentPage('diet-plan')}>
            View all days <ChevronRight className="w-4 h-4" />
          </Button>
        </div>

        <div className="space-y-4">
          {(() => {
            const dayKeys = ['sunday', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday'];
            const todayIndex = new Date().getDay();
            const todayPlan = state.dietPlan[dayKeys[todayIndex]];
            
            return [
              { title: 'Day', content: todayPlan.day },
              { title: 'Afternoon', content: todayPlan.afternoon },
              { title: 'Night', content: todayPlan.night },
              { title: 'General Lifestyle Guidance', content: todayPlan.lifestyle }
            ].map((section, index) => (
              <div key={index} className="border-b pb-4 last:border-b-0">
                <h3 className="text-sm font-medium text-gray-900 mb-2">{section.title}</h3>
                <p className="text-gray-700 text-sm">{section.content}</p>
              </div>
            ));
          })()}
        </div>

      </Card>

      {/* Today Activity */}
      <Card>
        <div className="flex items-start justify-between mb-4">
          <h2 className="text-lg font-medium text-gray-900">Today Activity</h2>
          <Button variant="ghost" onClick={() => setCurrentPage('activity')}>
            <Plus className="w-4 h-4" /> Update
          </Button>
        </div>
        
        <div className="overflow-x-auto">
          <table className="w-full">
            <thead>
              <tr className="border-b">
                <th className="text-left py-2 px-4 text-sm font-medium text-gray-700">Activity</th>
                <th className="text-center py-2 px-4 text-sm font-medium text-gray-700">Day</th>
                <th className="text-center py-2 px-4 text-sm font-medium text-gray-700">Afternoon</th>
                <th className="text-center py-2 px-4 text-sm font-medium text-gray-700">Night</th>
              </tr>
            </thead>
            <tbody>
              <tr className="border-b">
                <td className="py-3 px-4 text-sm text-gray-700">Food taken</td>
                <td className="text-center py-3 px-4">
                  {state.todayActivity.day.food ? '✓' : '—'}
                </td>
                <td className="text-center py-3 px-4">
                  {state.todayActivity.afternoon.food ? '✓' : '—'}
                </td>
                <td className="text-center py-3 px-4">
                  {state.todayActivity.night.food ? '✓' : '—'}
                </td>
              </tr>
              <tr className="border-b">
                <td className="py-3 px-4 text-sm text-gray-700">Medicine taken</td>
                <td className="text-center py-3 px-4">
                  {state.todayActivity.day.medicine ? '✓' : '—'}
                </td>
                <td className="text-center py-3 px-4">
                  {state.todayActivity.afternoon.medicine ? '✓' : '—'}
                </td>
                <td className="text-center py-3 px-4">
                  {state.todayActivity.night.medicine ? '✓' : '—'}
                </td>
              </tr>
              <tr>
                <td className="py-3 px-4 text-sm text-gray-700">Exercise</td>
                <td className="text-center py-3 px-4">
                  {state.todayActivity.day.exercise ? '✓' : '—'}
                </td>
                <td className="text-center py-3 px-4">
                </td>
                <td className="text-center py-3 px-4">
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </Card>

      {/* Test Upload */}
      <Card>
        <div className="flex items-start justify-between">
          <div>
            <h2 className="text-lg font-medium text-gray-900 mb-2">Test Upload</h2>
            <p className="text-sm text-gray-600">Update your latest test results</p>
          </div>
          <Button variant="ghost" onClick={() => setCurrentPage('test-upload')}>
            <Plus className="w-4 h-4" /> Upload
          </Button>
        </div>
      </Card>

      {/* Medication Plan */}
      <Card>
        <div className="flex items-start justify-between mb-4">
          <div>
            <h2 className="text-lg font-medium text-gray-900 mb-2">Medication Plan</h2>
            <p className="text-sm text-gray-600">
              Day: {state.medicationPlan.day} | Afternoon: {state.medicationPlan.afternoon} | Night: {state.medicationPlan.night}
            </p>
          </div>
          <Button variant="ghost" onClick={() => setCurrentPage('medication')}>
            <Plus className="w-4 h-4" /> Update
          </Button>
        </div>
        <Disclaimer text="Medication plans are entered as prescribed by your clinician." />
      </Card>
    </div>
  );
};

// ==================== SETTINGS PAGE ====================
const SettingsPage = () => {
  const { state, updateSettings, setCurrentPage } = useApp();
  const [username, setUsername] = useState(state.user.username);
  const [age, setAge] = useState(state.user.age);
  const [condition, setCondition] = useState(state.user.condition);
  const [region, setRegion] = useState(state.user.region);

  const handleSave = () => {
    updateSettings({ username, age: parseInt(age), condition, region });
    setCurrentPage('dashboard');
  };

  return (
    <div className="max-w-2xl">
      <div className="mb-6">
        <h1 className="text-2xl font-semibold text-gray-900">Settings</h1>
        <p className="text-gray-600 mt-1">Manage your profile information</p>
      </div>

      <Card>
        <Input
          label="Username"
          value={username}
          onChange={(e) => setUsername(e.target.value)}
          required
        />
        
        <Input
          label="Age"
          type="number"
          value={age}
          onChange={(e) => setAge(e.target.value)}
          required
        />
        
        <div className="mb-4">
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Condition <span className="text-red-500">*</span>
          </label>
          <select
            value={condition}
            onChange={(e) => setCondition(e.target.value)}
            className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-teal-500 min-h-[44px]"
          >
            <option value="diabetes">Diabetes</option>
            <option value="hypertension">Hypertension</option>
            <option value="both">Both</option>
          </select>
        </div>

        <div className="mb-4">
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Region/Country <span className="text-red-500">*</span>
          </label>
          <select
            value={region}
            onChange={(e) => setRegion(e.target.value)}
            className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-teal-500 min-h-[44px]"
          >
            <option value="">Select a country</option>
            {COUNTRIES.map((country) => (
              <option key={country} value={country}>
                {country}
              </option>
            ))}
          </select>
        </div>

        <div className="mb-6 p-4 bg-gray-50 rounded-lg">
          <h3 className="text-sm font-medium text-gray-700 mb-2">Health Thresholds</h3>
          <p className="text-sm text-gray-600">These values are managed by your healthcare provider and cannot be edited here.</p>
        </div>

        <div className="flex gap-3">
          <Button onClick={handleSave}>Save Changes</Button>
          <Button variant="secondary" onClick={() => setCurrentPage('dashboard')}>
            Cancel
          </Button>
        </div>
      </Card>
    </div>
  );
};

// ==================== FOOD & MEDICINE INTAKE PAGE ====================
const ActivityPage = () => {
  const { state, updateTodayActivity, setCurrentPage } = useApp();
  const [activity, setActivity] = useState(state.todayActivity);

  const handleToggle = (time, type) => {
    const newValue = !activity[time][type];
    setActivity(prev => ({
      ...prev,
      [time]: { ...prev[time], [type]: newValue }
    }));
    updateTodayActivity(time, type, newValue);
  };

  return (
    <div className="max-w-2xl">
      <div className="mb-6">
        <h1 className="text-2xl font-semibold text-gray-900">Today's Activity</h1>
        <p className="text-gray-600 mt-1">Track your daily food and medicine intake</p>
      </div>

      <Disclaimer text="This log resets daily. Use it to track your routine adherence." />

      <div className="space-y-4 mt-6">
        {['day', 'afternoon', 'night'].map((time) => (
          <Card key={time}>
            <h3 className="text-lg font-medium text-gray-900 mb-4 capitalize">{time}</h3>
            
            <div className="space-y-3">
              <label className="flex items-center gap-3 cursor-pointer">
                <input
                  type="checkbox"
                  checked={activity[time].food}
                  onChange={() => handleToggle(time, 'food')}
                  className="w-5 h-5 text-teal-600 rounded focus:ring-2 focus:ring-teal-500"
                />
                <span className="text-gray-700">Food taken</span>
              </label>
              
              <label className="flex items-center gap-3 cursor-pointer">
                <input
                  type="checkbox"
                  checked={activity[time].medicine}
                  onChange={() => handleToggle(time, 'medicine')}
                  className="w-5 h-5 text-teal-600 rounded focus:ring-2 focus:ring-teal-500"
                />
                <span className="text-gray-700">Medicine taken</span>
              </label>
              
              {time === 'day' && (
                <label className="flex items-center gap-3 cursor-pointer">
                  <input
                    type="checkbox"
                    checked={activity[time].exercise}
                    onChange={() => handleToggle(time, 'exercise')}
                    className="w-5 h-5 text-teal-600 rounded focus:ring-2 focus:ring-teal-500"
                  />
                  <span className="text-gray-700">Exercise</span>
                </label>
              )}
            </div>
          </Card>
        ))}
      </div>

      <div className="mt-6">
        <Button onClick={() => setCurrentPage('dashboard')}>
          Back to Dashboard
        </Button>
      </div>
    </div>
  );
};

// ==================== CURRENT DIET PLAN PAGE ====================
const DietPlanPage = () => {
  const { state, setCurrentPage, selectDay } = useApp();

  const dayKeys = ['sunday', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday'];
  const dayNames = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday'];
  const selectedPlan = state.dietPlan[dayKeys[state.selectedDay]];

  return (
    <div className="max-w-6xl">
      <div className="mb-6">
        <h1 className="text-2xl font-semibold text-gray-900">Diet Plan</h1>
        <p className="text-gray-600 mt-1">Select a day to view dietary guidance</p>
      </div>

     

      <div className="grid grid-cols-12 gap-6 mt-6">
        {/* Left narrow column for day selection */}
        <div className="col-span-2 space-y-2">
          {['SUN', 'MON', 'TUE', 'WED', 'THU', 'FRI', 'SAT'].map((dayName, index) => (
            <button
              key={dayName}
              onClick={() => selectDay(index)}
              className={`w-full py-3 px-3 text-sm font-medium rounded-lg transition-colors ${
                state.selectedDay === index
                  ? 'bg-teal-600 text-white shadow-md'
                  : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
              }`}
            >
              {dayName}
            </button>
          ))}
        </div>

        {/* Wide section for diet plan details */}
        <div className="col-span-10 space-y-4">
          <div className="mb-2">
            <h2 className="text-xl font-semibold text-gray-900">{dayNames[state.selectedDay]}'s Plan</h2>
          </div>

          <Card>
            <h3 className="text-lg font-medium text-gray-900 mb-3">Day</h3>
            <p className="text-gray-700">{selectedPlan.day}</p>
          </Card>

          <Card>
            <h3 className="text-lg font-medium text-gray-900 mb-3">Afternoon</h3>
            <p className="text-gray-700">{selectedPlan.afternoon}</p>
          </Card>

          <Card>
            <h3 className="text-lg font-medium text-gray-900 mb-3">Night</h3>
            <p className="text-gray-700">{selectedPlan.night}</p>
          </Card>

          <Card className="bg-blue-50 border border-blue-100">
            <h3 className="text-lg font-medium text-gray-900 mb-3">General Lifestyle Guidance</h3>
            <p className="text-gray-700">{selectedPlan.lifestyle}</p>
          </Card>
        </div>
      </div>

      <div className="mt-8">
        <Button onClick={() => setCurrentPage('dashboard')}>
          Back to Dashboard
        </Button>
      </div>
    </div>
  );
};

// ==================== TEST UPLOAD PAGE ====================
const TestUploadPage = () => {
  const { state, updateTestResult, setCurrentPage } = useApp();
  const [fastingSugar, setFastingSugar] = useState(state.lastTestResult.fastingSugar);
  const [postMealSugar, setPostMealSugar] = useState(state.lastTestResult.postMealSugar);

  const handleSubmit = () => {
    updateTestResult(parseFloat(fastingSugar), parseFloat(postMealSugar));
    setCurrentPage('dashboard');
  };

  return (
    <div className="max-w-2xl">
      <div className="mb-6">
        <h1 className="text-2xl font-semibold text-gray-900">Test Upload</h1>
        <p className="text-gray-600 mt-1">Update your latest test results</p>
      </div>

      <Card>
        <div className="mb-4">
          <Input
            label="Fasting Sugar (mg/dL)"
            type="number"
            value={fastingSugar}
            onChange={(e) => setFastingSugar(e.target.value)}
            required
            step="0.1"
          />
          <p className="text-xs text-gray-500 mt-1">Reference range: 70-100 mg/dL (informational only)</p>
        </div>

        <div className="mb-6">
          <Input
            label="Post-Meal Sugar (mg/dL)"
            type="number"
            value={postMealSugar}
            onChange={(e) => setPostMealSugar(e.target.value)}
            required
            step="0.1"
          />
          <p className="text-xs text-gray-500 mt-1">Reference range: 70-140 mg/dL (informational only)</p>
        </div>

        <div className="mb-6 p-4 bg-amber-50 border border-amber-100 rounded-lg">
          <p className="text-sm text-gray-700">
            <strong>Safety Note:</strong> If your values are very high or low, please contact your clinician immediately.
          </p>
        </div>

        <div className="flex gap-3">
          <Button onClick={handleSubmit}>Update Results</Button>
          <Button variant="secondary" onClick={() => setCurrentPage('dashboard')}>
            Cancel
          </Button>
        </div>
      </Card>
    </div>
  );
};

// ==================== MEDICATION PLAN PAGE ====================
const MedicationPlanPage = () => {
  const { state, updateMedicationPlan, setCurrentPage } = useApp();
  const [plan, setPlan] = useState(state.medicationPlan);

  const handleSubmit = () => {
    updateMedicationPlan({
      day: parseInt(plan.day),
      afternoon: parseInt(plan.afternoon),
      night: parseInt(plan.night)
    });
    setCurrentPage('dashboard');
  };

  return (
    <div className="max-w-2xl">
      <div className="mb-6">
        <h1 className="text-2xl font-semibold text-gray-900">Medication Plan</h1>
        <p className="text-gray-600 mt-1">Enter medication schedule as prescribed</p>
      </div>

      <Disclaimer text="Medication plans are entered as prescribed by your clinician." />

      <Card className="mt-6">
        <Input
          label="Day - Number of tablets"
          type="number"
          value={plan.day}
          onChange={(e) => setPlan({ ...plan, day: e.target.value })}
          required
          min="0"
        />

        <Input
          label="Afternoon - Number of tablets"
          type="number"
          value={plan.afternoon}
          onChange={(e) => setPlan({ ...plan, afternoon: e.target.value })}
          required
          min="0"
        />

        <Input
          label="Night - Number of tablets"
          type="number"
          value={plan.night}
          onChange={(e) => setPlan({ ...plan, night: e.target.value })}
          required
          min="0"
        />

        <div className="mb-6 p-4 bg-gray-50 rounded-lg">
          <h3 className="text-sm font-medium text-gray-700 mb-2">Current Schedule</h3>
          <p className="text-sm text-gray-600">
            Day: {plan.day} tablet(s) | Afternoon: {plan.afternoon} tablet(s) | Night: {plan.night} tablet(s)
          </p>
        </div>

        <div className="flex gap-3">
          <Button onClick={handleSubmit}>Save Plan</Button>
          <Button variant="secondary" onClick={() => setCurrentPage('dashboard')}>
            Cancel
          </Button>
        </div>
      </Card>
    </div>
  );
};

// ==================== LAYOUT ====================
const Layout = ({ children }) => {
  const { logout, setCurrentPage, currentPage } = useApp();

  return (
    <div className="min-h-screen bg-gray-50 flex">
      {/* Sidebar */}
      <div className="w-20 bg-white border-r border-gray-200 flex flex-col items-center py-6 sticky top-0 h-screen">
        <div className="w-12 h-12 bg-teal-600 rounded-lg flex items-center justify-center mb-8">
          <Activity className="w-6 h-6 text-white" />
        </div>
        
        <nav className="flex-1 flex flex-col gap-4">
          <button
            onClick={() => setCurrentPage('dashboard')}
            className={`w-12 h-12 rounded-lg flex items-center justify-center transition-colors ${
              currentPage === 'dashboard' ? 'bg-teal-50 text-teal-600' : 'text-gray-600 hover:bg-gray-50'
            }`}
            aria-label="Dashboard"
          >
            <Home className="w-5 h-5" />
          </button>
        </nav>
        
        <div className="flex flex-col gap-4">
          <button
            onClick={() => setCurrentPage('settings')}
            className={`w-12 h-12 rounded-lg flex items-center justify-center transition-colors ${
              currentPage === 'settings' ? 'bg-teal-50 text-teal-600' : 'text-gray-600 hover:bg-gray-50'
            }`}
            aria-label="Settings"
          >
            <Settings className="w-5 h-5" />
          </button>
          
          <button
            onClick={logout}
            className="w-12 h-12 rounded-lg flex items-center justify-center text-gray-600 hover:bg-gray-50 transition-colors"
            aria-label="Logout"
          >
            <LogOut className="w-5 h-5" />
          </button>
        </div>
      </div>

      {/* Main Content */}
      <div className="flex-1 overflow-auto">
        <div className="max-w-6xl mx-auto p-8">
          {children}
        </div>
      </div>
    </div>
  );
};

// ==================== MAIN APP ====================
const App = () => {
  const { state, currentPage } = useApp();

  if (!state.user.isAuthenticated) {
    return <LoginPage />;
  }

  const pages = {
    dashboard: <DashboardPage />,
    settings: <SettingsPage />,
    activity: <ActivityPage />,
    'diet-plan': <DietPlanPage />,
    'test-upload': <TestUploadPage />,
    medication: <MedicationPlanPage />
  };

  return (
    <Layout>
      {pages[currentPage] || <DashboardPage />}
    </Layout>
  );
};

// ==================== ROOT ====================
export default function Root() {
  return (
    <AppProvider>
      <App />
    </AppProvider>
  );
}
