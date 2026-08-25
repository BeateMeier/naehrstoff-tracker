<!DOCTYPE html>
<html lang="de">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Nährstoff-Tracker & Tagesbedarf Übersicht</title>
    <!-- Tailwind CSS -->
    <script src="https://cdn.tailwindcss.com"></script>
    <!-- FontAwesome Icons -->
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.1/css/all.min.css">
    <!-- Google Fonts -->
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap" rel="stylesheet">

    <style>
        body {
            font-family: 'Inter', sans-serif;
            background-color: #f8fafc;
            color: #0f172a;
        }
        .custom-scrollbar::-webkit-scrollbar {
            width: 6px;
            height: 6px;
        }
        .custom-scrollbar::-webkit-scrollbar-track {
            background: #f1f5f9;
        }
        .custom-scrollbar::-webkit-scrollbar-thumb {
            background: #cbd5e1;
            border-radius: 4px;
        }
        .custom-scrollbar::-webkit-scrollbar-thumb:hover {
            background: #94a3b8;
        }
    </style>
</head>
<body class="min-h-screen flex flex-col">

    <!-- Header Navigation -->
    <header class="bg-slate-900 text-white shadow-md sticky top-0 z-50">
        <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 flex justify-between items-center h-16">
            <div class="flex items-center space-x-3">
                <div class="bg-emerald-500 text-slate-900 p-2 rounded-lg font-bold">
                    <i class="fa-solid fa-apple-whole text-xl"></i>
                </div>
                <div>
                    <h1 class="text-lg font-bold leading-tight">NährstoffTracker Pro</h1>
                    <p class="text-xs text-slate-400">Tagesbedarf & Verzehranalyse</p>
                </div>
            </div>

            <!-- Profile / Gender Quick Filter -->
            <div class="flex items-center space-x-4">
                <div class="flex items-center bg-slate-800 rounded-lg p-1 text-xs border border-slate-700">
                    <span class="px-2 text-slate-400">Referenzwerte:</span>
                    <button id="profileMaleBtn" onclick="setProfile('m')" class="px-3 py-1 rounded-md font-medium transition-colors bg-emerald-500 text-slate-950 shadow">
                        <i class="fa-solid fa-mars mr-1"></i> Männlich
                    </button>
                    <button id="profileFemaleBtn" onclick="setProfile('w')" class="px-3 py-1 rounded-md font-medium text-slate-300 hover:text-white transition-colors">
                        <i class="fa-solid fa-venus mr-1"></i> Weiblich
                    </button>
                </div>
                <button onclick="resetTodayData()" class="text-xs bg-slate-800 hover:bg-slate-700 text-slate-300 px-3 py-2 rounded-lg border border-slate-700 transition">
                    <i class="fa-solid fa-rotate-left mr-1"></i> Tag zurücksetzen
                </button>
            </div>
        </div>

        <!-- Tab Bar -->
        <div class="bg-slate-800 border-t border-slate-700 px-4 sm:px-6 lg:px-8">
            <div class="max-w-7xl mx-auto flex space-x-1 sm:space-x-4 overflow-x-auto">
                <button id="tabNavOverview" onclick="switchTab('overview')" class="px-4 py-3 text-sm font-semibold border-b-2 border-emerald-400 text-emerald-400 flex items-center space-x-2 whitespace-nowrap">
                    <i class="fa-solid fa-list-check"></i>
                    <span>Alle Nährstoffe (Tagesvergleich)</span>
                </button>
                <button id="tabNavLog" onclick="switchTab('log')" class="px-4 py-3 text-sm font-semibold border-b-2 border-transparent text-slate-400 hover:text-slate-200 flex items-center space-x-2 whitespace-nowrap">
                    <i class="fa-solid fa-utensils"></i>
                    <span>Heute konsumiert / Lebensmittel eintragen</span>
                </button>
                <button id="tabNavExcel" onclick="switchTab('excel')" class="px-4 py-3 text-sm font-semibold border-b-2 border-transparent text-slate-400 hover:text-slate-200 flex items-center space-x-2 whitespace-nowrap">
                    <i class="fa-solid fa-file-excel"></i>
                    <span>Excel Export & Import</span>
                </button>
            </div>
        </div>
    </header>

    <!-- Main Content Container -->
    <main class="flex-1 max-w-7xl w-full mx-auto px-4 sm:px-6 lg:px-8 py-6">

        <!-- TAB 1: ALLE NÄHRSTOFFE / TAGESVERGLEICH -->
        <section id="tabOverview" class="space-y-6">
            
            <!-- Summary Stats Banner -->
            <div class="grid grid-cols-1 md:grid-cols-4 gap-4">
                <div class="bg-white p-5 rounded-xl border border-slate-200 shadow-sm flex items-center space-x-4">
                    <div class="w-12 h-12 rounded-full bg-amber-100 text-amber-600 flex items-center justify-center text-xl">
                        <i class="fa-solid fa-bolt"></i>
                    </div>
                    <div>
                        <div class="text-xs text-slate-500 font-medium">Energie (Kalorien)</div>
                        <div class="text-xl font-bold text-slate-900" id="summaryCalories">0 / 2200 kcal</div>
                        <div class="w-32 bg-slate-100 h-1.5 rounded-full mt-1.5 overflow-hidden">
                            <div id="summaryCaloriesBar" class="bg-amber-500 h-full w-0"></div>
                        </div>
                    </div>
                </div>

                <div class="bg-white p-5 rounded-xl border border-slate-200 shadow-sm flex items-center space-x-4">
                    <div class="w-12 h-12 rounded-full bg-blue-100 text-blue-600 flex items-center justify-center text-xl">
                        <i class="fa-solid fa-drumstick-bite"></i>
                    </div>
                    <div>
                        <div class="text-xs text-slate-500 font-medium">Protein (Eiweiß)</div>
                        <div class="text-xl font-bold text-slate-900" id="summaryProtein">0 / 70 g</div>
                        <div class="w-32 bg-slate-100 h-1.5 rounded-full mt-1.5 overflow-hidden">
                            <div id="summaryProteinBar" class="bg-blue-500 h-full w-0"></div>
                        </div>
                    </div>
                </div>

                <div class="bg-white p-5 rounded-xl border border-slate-200 shadow-sm flex items-center space-x-4">
                    <div class="w-12 h-12 rounded-full bg-emerald-100 text-emerald-600 flex items-center justify-center text-xl">
                        <i class="fa-solid fa-pills"></i>
                    </div>
                    <div>
                        <div class="text-xs text-slate-500 font-medium">Vitamine gedeckt</div>
                        <div class="text-xl font-bold text-slate-900" id="summaryVitaminsCount">0 / 13</div>
                        <div class="text-xs text-emerald-600 font-medium mt-1" id="summaryVitaminsPct">0% im Soll</div>
                    </div>
                </div>

                <div class="bg-white p-5 rounded-xl border border-slate-200 shadow-sm flex items-center space-x-4">
                    <div class="w-12 h-12 rounded-full bg-purple-100 text-purple-600 flex items-center justify-center text-xl">
                        <i class="fa-solid fa-gem"></i>
                    </div>
                    <div>
                        <div class="text-xs text-slate-500 font-medium">Mineralstoffe gedeckt</div>
                        <div class="text-xl font-bold text-slate-900" id="summaryMineralsCount">0 / 11</div>
                        <div class="text-xs text-purple-600 font-medium mt-1" id="summaryMineralsPct">0% im Soll</div>
                    </div>
                </div>
            </div>

            <!-- Controls & Category Filters -->
            <div class="bg-white p-4 rounded-xl border border-slate-200 shadow-sm flex flex-col md:flex-row justify-between items-center gap-4">
                <div class="flex flex-wrap items-center gap-2 w-full md:w-auto">
                    <span class="text-xs font-semibold text-slate-400 uppercase tracking-wider mr-2">Kategorie:</span>
                    <button onclick="filterCategory('all')" id="catBtn-all" class="cat-filter-btn px-3 py-1.5 rounded-lg text-xs font-semibold bg-slate-900 text-white">Alle Nährstoffe</button>
                    <button onclick="filterCategory('macro')" id="catBtn-macro" class="cat-filter-btn px-3 py-1.5 rounded-lg text-xs font-medium bg-slate-100 text-slate-700 hover:bg-slate-200">Makronährstoffe</button>
                    <button onclick="filterCategory('vit-fat')" id="catBtn-vit-fat" class="cat-filter-btn px-3 py-1.5 rounded-lg text-xs font-medium bg-slate-100 text-slate-700 hover:bg-slate-200">Vitamine (Fettlöslich)</button>
                    <button onclick="filterCategory('vit-water')" id="catBtn-vit-water" class="cat-filter-btn px-3 py-1.5 rounded-lg text-xs font-medium bg-slate-100 text-slate-700 hover:bg-slate-200">Vitamine (Wasserlöslich)</button>
                    <button onclick="filterCategory('minerals')" id="catBtn-minerals" class="cat-filter-btn px-3 py-1.5 rounded-lg text-xs font-medium bg-slate-100 text-slate-700 hover:bg-slate-200">Mineralstoffe & Spurenelemente</button>
                </div>

                <div class="relative w-full md:w-64">
                    <i class="fa-solid fa-magnifying-glass absolute left-3 top-3 text-slate-400 text-xs"></i>
                    <input type="text" id="nutrientSearchInput" oninput="renderNutrientsTable()" placeholder="Nährstoff suchen..." class="w-full pl-9 pr-3 py-2 text-xs rounded-lg border border-slate-300 focus:outline-none focus:ring-2 focus:ring-emerald-500 focus:border-transparent">
                </div>
            </div>

            <!-- Main Table Card -->
            <div class="bg-white rounded-xl border border-slate-200 shadow-sm overflow-hidden">
                <div class="overflow-x-auto custom-scrollbar">
                    <table class="w-full text-left border-collapse">
                        <thead>
                            <tr class="bg-slate-50 border-b border-slate-200 text-xs text-slate-500 font-semibold uppercase tracking-wider">
                                <th class="py-3.5 px-4">Nährstoff</th>
                                <th class="py-3.5 px-4 text-center">Empfohlener Tagesbedarf (DGE)</th>
                                <th class="py-3.5 px-4 text-center">Heute konsumiert</th>
                                <th class="py-3.5 px-4">Fortschritt / Status</th>
                                <th class="py-3.5 px-4 text-right">Differenz</th>
                                <th class="py-3.5 px-4 text-center">Schnellanpassung</th>
                            </tr>
                        </thead>
                        <tbody id="nutrientsTableBody" class="divide-y divide-slate-100 text-sm">
                            <!-- Rows generated by JS -->
                        </tbody>
                    </table>
                </div>
            </div>
        </section>

        <!-- TAB 2: HEUTE KONSUMIERT / LEBENSMITTEL LOG -->
        <section id="tabLog" class="hidden space-y-6">
            <div class="grid grid-cols-1 lg:grid-cols-3 gap-6">
                
                <!-- Quick Meal Logger -->
                <div class="bg-white p-6 rounded-xl border border-slate-200 shadow-sm lg:col-span-1 space-y-4">
                    <h3 class="font-bold text-slate-900 text-base flex items-center space-x-2">
                        <i class="fa-solid fa-plus-circle text-emerald-500"></i>
                        <span>Schnell-Eingabe Verzehr</span>
                    </h3>
                    <p class="text-xs text-slate-500">Wähle ein vordefiniertes Lebensmittel oder gib Nährstoffe direkt ein.</p>
                    
                    <div class="space-y-3">
                        <div>
                            <label class="block text-xs font-semibold text-slate-700 mb-1">Lebensmittel-Vorlage wählen</label>
                            <select id="presetFoodSelect" onchange="loadPresetFood()" class="w-full p-2.5 text-xs bg-slate-50 border border-slate-300 rounded-lg focus:ring-2 focus:ring-emerald-500">
                                <option value="">-- Eigenen Wert / Vorlage wählen --</option>
                                <option value="haferflocken">Haferflocken (100g) - Zink, Magnesium, B1</option>
                                <option value="lachs">Lachsfilet (150g) - Omega 3, Vit D, B12</option>
                                <option value="orange">Orange (150g) - Vitamin C, Folsäure</option>
                                <option value="spinat">Blattspinat (200g) - Eisen, Vit A, Magnesium</option>
                                <option value="mandeln">Mandeln (30g) - Vitamin E, Calcium, Magnesium</option>
                                <option value="milch">Vollmilch (250ml) - Calcium, B2, Protein</option>
                                <option value="apfel">Apfel (180g) - Vit C, Ballaststoffe</option>
                            </select>
                        </div>

                        <div class="pt-2 border-t border-slate-100">
                            <label class="block text-xs font-semibold text-slate-700 mb-1">Nährstoff auswählen</label>
                            <select id="logNutrientSelect" class="w-full p-2.5 text-xs border border-slate-300 rounded-lg focus:ring-2 focus:ring-emerald-500">
                                <!-- Populated by JS -->
                            </select>
                        </div>

                        <div>
                            <label class="block text-xs font-semibold text-slate-700 mb-1">Menge hinzufügen (+)</label>
                            <input type="number" id="logNutrientAmount" step="0.1" placeholder="z.B. 15" class="w-full p-2.5 text-xs border border-slate-300 rounded-lg focus:ring-2 focus:ring-emerald-500">
                        </div>

                        <button onclick="addSingleNutrientLog()" class="w-full py-2.5 bg-emerald-600 hover:bg-emerald-700 text-white font-medium text-xs rounded-lg transition shadow">
                            <i class="fa-solid fa-plus mr-1"></i> Wert hinzufügen
                        </button>
                    </div>

                    <div class="pt-4 border-t border-slate-100">
                        <h4 class="text-xs font-bold text-slate-700 mb-2">Beliebte Superfoods hinzufügen:</h4>
                        <div class="flex flex-wrap gap-1.5">
                            <button onclick="addPresetDirect('haferflocken')" class="px-2.5 py-1 bg-slate-100 hover:bg-emerald-50 hover:text-emerald-700 text-slate-700 rounded text-xs border border-slate-200 transition">+ Haferflocken 100g</button>
                            <button onclick="addPresetDirect('orange')" class="px-2.5 py-1 bg-slate-100 hover:bg-emerald-50 hover:text-emerald-700 text-slate-700 rounded text-xs border border-slate-200 transition">+ 1 Orange</button>
                            <button onclick="addPresetDirect('spinat')" class="px-2.5 py-1 bg-slate-100 hover:bg-emerald-50 hover:text-emerald-700 text-slate-700 rounded text-xs border border-slate-200 transition">+ Spinat 200g</button>
                            <button onclick="addPresetDirect('mandeln')" class="px-2.5 py-1 bg-slate-100 hover:bg-emerald-50 hover:text-emerald-700 text-slate-700 rounded text-xs border border-slate-200 transition">+ Mandeln 30g</button>
                        </div>
                    </div>
                </div>

                <!-- Logged Meals History Table -->
                <div class="bg-white p-6 rounded-xl border border-slate-200 shadow-sm lg:col-span-2 space-y-4">
                    <div class="flex justify-between items-center">
                        <h3 class="font-bold text-slate-900 text-base flex items-center space-x-2">
                            <i class="fa-solid fa-clock-rotate-left text-blue-500"></i>
                            <span>Heutiges Verzehrprotokoll</span>
                        </h3>
                        <span id="logCountBadge" class="text-xs bg-slate-100 text-slate-600 font-semibold px-2.5 py-1 rounded-full">0 Einträge</span>
                    </div>

                    <div class="overflow-x-auto">
                        <table class="w-full text-left text-xs">
                            <thead>
                                <tr class="bg-slate-50 border-b border-slate-200 text-slate-500 font-semibold uppercase">
                                    <th class="py-2.5 px-3">Uhrzeit</th>
                                    <th class="py-2.5 px-3">Lebensmittel / Eintrag</th>
                                    <th class="py-2.5 px-3">Enthaltene Hauptnährstoffe</th>
                                    <th class="py-2.5 px-3 text-right">Aktion</th>
                                </tr>
                            </thead>
                            <tbody id="logHistoryTableBody" class="divide-y divide-slate-100">
                                <!-- Log history items -->
                            </tbody>
                        </table>
                    </div>
                </div>
            </div>
        </section>

        <!-- TAB 3: EXCEL EXPORT & IMPORT -->
        <section id="tabExcel" class="hidden space-y-6">
            <div class="bg-white p-6 rounded-xl border border-slate-200 shadow-sm space-y-6 max-w-3xl mx-auto">
                <div>
                    <h3 class="font-bold text-slate-900 text-base flex items-center space-x-2">
                        <i class="fa-solid fa-file-excel text-emerald-600"></i>
                        <span>Excel Daten-Export & Schnittstelle</span>
                    </h3>
                    <p class="text-xs text-slate-500 mt-1">Exportiere alle Nährstoffe samt Soll-Empfehlung und konsumierter Tagesmenge direkt als Excel-kompatible CSV-Datei.</p>
                </div>

                <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
                    <div class="p-4 rounded-xl border border-emerald-100 bg-emerald-50/50 space-y-3">
                        <div class="text-emerald-800 font-bold text-sm flex items-center">
                            <i class="fa-solid fa-download mr-2"></i> CSV / Excel Export
                        </div>
                        <p class="text-xs text-slate-600">Lade deinen aktuellen Tagesstand mit allen Referenzwerten als CSV herunter. Perfekt zur Weiterverarbeitung in Microsoft Excel.</p>
                        <button onclick="exportToExcelCSV()" class="w-full py-2 bg-emerald-600 hover:bg-emerald-700 text-white font-medium text-xs rounded-lg transition shadow">
                            <i class="fa-solid fa-file-csv mr-1"></i> Tageswerte als CSV exportieren
                        </button>
                    </div>

                    <div class="p-4 rounded-xl border border-blue-100 bg-blue-50/50 space-y-3">
                        <div class="text-blue-800 font-bold text-sm flex items-center">
                            <i class="fa-solid fa-upload mr-2"></i> CSV / Excel Import
                        </div>
                        <p class="text-xs text-slate-600">Lade eine exportierte CSV-Datei hoch, um die konsumierten Werte oder Referenzmengen zu aktualisieren.</p>
                        <input type="file" id="csvFileInput" accept=".csv" class="hidden" onchange="importFromCSV(event)">
                        <button onclick="document.getElementById('csvFileInput').click()" class="w-full py-2 bg-blue-600 hover:bg-blue-700 text-white font-medium text-xs rounded-lg transition shadow">
                            <i class="fa-solid fa-folder-open mr-1"></i> CSV-Datei auswählen
                        </button>
                    </div>
                </div>

                <!-- Data Preview Code Box -->
                <div class="pt-4 border-t border-slate-100">
                    <label class="block text-xs font-semibold text-slate-700 mb-2">Vorschau der Export-Struktur (CSV/Excel Datenfeld):</label>
                    <textarea id="csvPreviewArea" readonly class="w-full h-40 p-3 bg-slate-900 text-slate-200 font-mono text-xs rounded-lg custom-scrollbar focus:outline-none"></textarea>
                </div>
            </div>
        </section>

    </main>

    <!-- Footer -->
    <footer class="bg-white border-t border-slate-200 py-4 text-center text-xs text-slate-400">
        Nährstoff-Tracker &copy; 2026 | Referenzwerte nach DGE/ÖGE (Deutsche Gesellschaft für Ernährung)
    </footer>

    <!-- JAVASCRIPT LOGIC -->
    <script>
        // DGE Daily Recommended Intake Database
        const nutrientDatabase = [
            // Makronährstoffe
            { id: 'kcal', name: 'Energie (Kalorien)', cat: 'macro', unit: 'kcal', rdaM: 2200, rdaW: 1800, consumed: 0, icon: 'fa-bolt', color: 'amber' },
            { id: 'protein', name: 'Protein (Eiweiß)', cat: 'macro', unit: 'g', rdaM: 70, rdaW: 60, consumed: 0, icon: 'fa-drumstick-bite', color: 'blue' },
            { id: 'carbs', name: 'Kohlenhydrate', cat: 'macro', unit: 'g', rdaM: 260, rdaW: 230, consumed: 0, icon: 'fa-wheat-awn', color: 'yellow' },
            { id: 'fat', name: 'Fett (Gesamt)', cat: 'macro', unit: 'g', rdaM: 70, rdaW: 60, consumed: 0, icon: 'fa-oil-well', color: 'orange' },
            { id: 'fiber', name: 'Ballaststoffe', cat: 'macro', unit: 'g', rdaM: 30, rdaW: 30, consumed: 0, icon: 'fa-seedling', color: 'emerald' },
            { id: 'water', name: 'Wasser / Flüssigkeit', cat: 'macro', unit: 'ml', rdaM: 2500, rdaW: 2000, consumed: 0, icon: 'fa-glass-water', color: 'cyan' },

            // Fettlösliche Vitamine
            { id: 'vitA', name: 'Vitamin A (Retinol)', cat: 'vit-fat', unit: 'µg', rdaM: 850, rdaW: 700, consumed: 0, icon: 'fa-eye', color: 'orange' },
            { id: 'vitD', name: 'Vitamin D (Calciferol)', cat: 'vit-fat', unit: 'µg', rdaM: 20, rdaW: 20, consumed: 0, icon: 'fa-sun', color: 'yellow' },
            { id: 'vitE', name: 'Vitamin E (Tocopherol)', cat: 'vit-fat', unit: 'mg', rdaM: 14, rdaW: 12, consumed: 0, icon: 'fa-shield-halved', color: 'green' },
            { id: 'vitK', name: 'Vitamin K (Phyllochinon)', cat: 'vit-fat', unit: 'µg', rdaM: 70, rdaW: 60, consumed: 0, icon: 'fa-leaf', color: 'emerald' },

            // Wasserlösliche Vitamine
            { id: 'vitC', name: 'Vitamin C (Ascorbinsäure)', cat: 'vit-water', unit: 'mg', rdaM: 110, rdaW: 95, consumed: 0, icon: 'fa-lemon', color: 'yellow' },
            { id: 'vitB1', name: 'Vitamin B1 (Thiamin)', cat: 'vit-water', unit: 'mg', rdaM: 1.2, rdaW: 1.0, consumed: 0, icon: 'fa-vial', color: 'sky' },
            { id: 'vitB2', name: 'Vitamin B2 (Riboflavin)', cat: 'vit-water', unit: 'mg', rdaM: 1.4, rdaW: 1.1, consumed: 0, icon: 'fa-vial', color: 'sky' },
            { id: 'vitB3', name: 'Vitamin B3 (Niacin)', cat: 'vit-water', unit: 'mg', rdaM: 15, rdaW: 12, consumed: 0, icon: 'fa-vial', color: 'sky' },
            { id: 'vitB5', name: 'Vitamin B5 (Pantothensäure)', cat: 'vit-water', unit: 'mg', rdaM: 5.0, rdaW: 5.0, consumed: 0, icon: 'fa-vial', color: 'sky' },
            { id: 'vitB6', name: 'Vitamin B6 (Pyridoxin)', cat: 'vit-water', unit: 'mg', rdaM: 1.6, rdaW: 1.4, consumed: 0, icon: 'fa-vial', color: 'sky' },
            { id: 'vitB7', name: 'Vitamin B7 (Biotin)', cat: 'vit-water', unit: 'µg', rdaM: 45, rdaW: 45, consumed: 0, icon: 'fa-vial', color: 'sky' },
            { id: 'vitB9', name: 'Vitamin B9 (Folsäure)', cat: 'vit-water', unit: 'µg', rdaM: 300, rdaW: 300, consumed: 0, icon: 'fa-vial', color: 'sky' },
            { id: 'vitB12', name: 'Vitamin B12 (Cobalamin)', cat: 'vit-water', unit: 'µg', rdaM: 4.0, rdaW: 4.0, consumed: 0, icon: 'fa-vial', color: 'sky' },

            // Mineralstoffe & Spurenelemente
            { id: 'calcium', name: 'Calcium (Kalzium)', cat: 'minerals', unit: 'mg', rdaM: 1000, rdaW: 1000, consumed: 0, icon: 'fa-bone', color: 'slate' },
            { id: 'magnesium', name: 'Magnesium', cat: 'minerals', unit: 'mg', rdaM: 350, rdaW: 300, consumed: 0, icon: 'fa-bolt-lightning', color: 'indigo' },
            { id: 'potassium', name: 'Kalium', cat: 'minerals', unit: 'mg', rdaM: 4000, rdaW: 4000, consumed: 0, icon: 'fa-heart-pulse', color: 'red' },
            { id: 'sodium', name: 'Natrium', cat: 'minerals', unit: 'mg', rdaM: 1500, rdaW: 1500, consumed: 0, icon: 'fa-cubes-stacked', color: 'zinc' },
            { id: 'iron', name: 'Eisen', cat: 'minerals', unit: 'mg', rdaM: 11, rdaW: 16, consumed: 0, icon: 'fa-magnet', color: 'red' },
            { id: 'zinc', name: 'Zink', cat: 'minerals', unit: 'mg', rdaM: 14, rdaW: 10, consumed: 0, icon: 'fa-shield', color: 'purple' },
            { id: 'iodine', name: 'Jod', cat: 'minerals', unit: 'µg', rdaM: 200, rdaW: 200, consumed: 0, icon: 'fa-fish', color: 'blue' },
            { id: 'selenium', name: 'Selen', cat: 'minerals', unit: 'µg', rdaM: 70, rdaW: 60, consumed: 0, icon: 'fa-atom', color: 'teal' },
            { id: 'phosphorus', name: 'Phosphor', cat: 'minerals', unit: 'mg', rdaM: 550, rdaW: 550, consumed: 0, icon: 'fa-circle-nodes', color: 'stone' },
            { id: 'copper', name: 'Kupfer', cat: 'minerals', unit: 'mg', rdaM: 1.2, rdaW: 1.2, consumed: 0, icon: 'fa-coins', color: 'amber' },
            { id: 'manganese', name: 'Mangan', cat: 'minerals', unit: 'mg', rdaM: 3.0, rdaW: 3.0, consumed: 0, icon: 'fa-cubes', color: 'emerald' }
        ];

        // Food Presets Data
        const foodPresets = {
            haferflocken: { name: 'Haferflocken (100g)', nutrients: { kcal: 370, protein: 13, carbs: 59, fat: 7, fiber: 10, vitB1: 0.6, magnesium: 130, zinc: 4.0, iron: 4.5 } },
            lachs: { name: 'Lachsfilet (150g)', nutrients: { kcal: 310, protein: 30, fat: 20, vitD: 16, vitB12: 4.5, selenium: 40, potassium: 500 } },
            orange: { name: 'Frische Orange (150g)', nutrients: { kcal: 70, carbs: 14, fiber: 3, vitC: 80, vitB9: 45, potassium: 250 } },
            spinat: { name: 'Blattspinat gekocht (200g)', nutrients: { kcal: 45, protein: 5, fiber: 5, vitA: 900, vitK: 450, vitC: 50, iron: 5.5, magnesium: 160 } },
            mandeln: { name: 'Mandeln (30g)', nutrients: { kcal: 175, protein: 6, fat: 15, fiber: 4, vitE: 7.5, calcium: 80, magnesium: 80 } },
            milch: { name: 'Vollmilch (250ml)', nutrients: { kcal: 160, protein: 8, carbs: 12, fat: 9, calcium: 300, vitB2: 0.4, vitB12: 1.1 } },
            apfel: { name: 'Apfel mit Schale (180g)', nutrients: { kcal: 95, carbs: 22, fiber: 4, vitC: 12, potassium: 190 } }
        };

        // App State
        let currentGender = 'm';
        let currentCategory = 'all';
        let foodLogs = [];

        // Initialize App
        document.addEventListener('DOMContentLoaded', () => {
            loadFromLocalStorage();
            populateSelectOptions();
            renderNutrientsTable();
            renderLogHistory();
            updateSummaryCards();
            updateCsvPreview();
        });

        // Set Active Profile / Gender
        function setProfile(gender) {
            currentGender = gender;
            const maleBtn = document.getElementById('profileMaleBtn');
            const femaleBtn = document.getElementById('profileFemaleBtn');

            if (gender === 'm') {
                maleBtn.className = "px-3 py-1 rounded-md font-medium transition-colors bg-emerald-500 text-slate-950 shadow";
                femaleBtn.className = "px-3 py-1 rounded-md font-medium text-slate-300 hover:text-white transition-colors";
            } else {
                femaleBtn.className = "px-3 py-1 rounded-md font-medium transition-colors bg-emerald-500 text-slate-950 shadow";
                maleBtn.className = "px-3 py-1 rounded-md font-medium text-slate-300 hover:text-white transition-colors";
            }
            renderNutrientsTable();
            updateSummaryCards();
            updateCsvPreview();
            saveToLocalStorage();
        }

        // Switch Tabs
        function switchTab(tabId) {
            document.getElementById('tabOverview').classList.add('hidden');
            document.getElementById('tabLog').classList.add('hidden');
            document.getElementById('tabExcel').classList.add('hidden');

            document.getElementById('tabNavOverview').className = "px-4 py-3 text-sm font-semibold border-b-2 border-transparent text-slate-400 hover:text-slate-200 flex items-center space-x-2 whitespace-nowrap";
            document.getElementById('tabNavLog').className = "px-4 py-3 text-sm font-semibold border-b-2 border-transparent text-slate-400 hover:text-slate-200 flex items-center space-x-2 whitespace-nowrap";
            document.getElementById('tabNavExcel').className = "px-4 py-3 text-sm font-semibold border-b-2 border-transparent text-slate-400 hover:text-slate-200 flex items-center space-x-2 whitespace-nowrap";

            if (tabId === 'overview') {
                document.getElementById('tabOverview').classList.remove('hidden');
                document.getElementById('tabNavOverview').className = "px-4 py-3 text-sm font-semibold border-b-2 border-emerald-400 text-emerald-400 flex items-center space-x-2 whitespace-nowrap";
            } else if (tabId === 'log') {
                document.getElementById('tabLog').classList.remove('hidden');
                document.getElementById('tabNavLog').className = "px-4 py-3 text-sm font-semibold border-b-2 border-emerald-400 text-emerald-400 flex items-center space-x-2 whitespace-nowrap";
            } else if (tabId === 'excel') {
                document.getElementById('tabExcel').classList.remove('hidden');
                document.getElementById('tabNavExcel').className = "px-4 py-3 text-sm font-semibold border-b-2 border-emerald-400 text-emerald-400 flex items-center space-x-2 whitespace-nowrap";
                updateCsvPreview();
            }
        }

        // Filter Category Buttons
        function filterCategory(cat) {
            currentCategory = cat;
            document.querySelectorAll('.cat-filter-btn').forEach(btn => {
                btn.className = "cat-filter-btn px-3 py-1.5 rounded-lg text-xs font-medium bg-slate-100 text-slate-700 hover:bg-slate-200";
            });
            const activeBtn = document.getElementById(`catBtn-${cat}`);
            if (activeBtn) {
                activeBtn.className = "cat-filter-btn px-3 py-1.5 rounded-lg text-xs font-semibold bg-slate-900 text-white";
            }
            renderNutrientsTable();
        }

        // Populate Dropdowns
        function populateSelectOptions() {
            const select = document.getElementById('logNutrientSelect');
            select.innerHTML = '';
            nutrientDatabase.forEach(item => {
                const option = document.createElement('option');
                option.value = item.id;
                option.textContent = `${item.name} (${item.unit})`;
                select.appendChild(option);
            });
        }

        // Render Overview Table
        function renderNutrientsTable() {
            const tbody = document.getElementById('nutrientsTableBody');
            tbody.innerHTML = '';

            const searchTerm = document.getElementById('nutrientSearchInput').value.toLowerCase();

            const filtered = nutrientDatabase.filter(item => {
                const matchesCat = (currentCategory === 'all') || (item.cat === currentCategory);
                const matchesSearch = item.name.toLowerCase().includes(searchTerm) || item.unit.toLowerCase().includes(searchTerm);
                return matchesCat && matchesSearch;
            });

            if (filtered.length === 0) {
                tbody.innerHTML = `<tr><td colspan="6" class="py-8 text-center text-slate-400 text-xs">Keine Nährstoffe gefunden.</td></tr>`;
                return;
            }

            filtered.forEach(item => {
                const targetVal = currentGender === 'm' ? item.rdaM : item.rdaW;
                const consumedVal = item.consumed || 0;
                const pct = Math.min(Math.round((consumedVal / targetVal) * 100), 200);
                const diff = (consumedVal - targetVal).toFixed(1);

                let statusBadge = '';
                let barColor = 'bg-emerald-500';

                if (pct >= 100) {
                    statusBadge = `<span class="px-2 py-0.5 rounded-full text-[10px] font-bold bg-emerald-100 text-emerald-800"><i class="fa-solid fa-check mr-1"></i>Gedeckt (${pct}%)</span>`;
                    barColor = 'bg-emerald-500';
                } else if (pct >= 50) {
                    statusBadge = `<span class="px-2 py-0.5 rounded-full text-[10px] font-bold bg-amber-100 text-amber-800"><i class="fa-solid fa-spinner mr-1"></i>Teilweise (${pct}%)</span>`;
                    barColor = 'bg-amber-400';
                } else {
                    statusBadge = `<span class="px-2 py-0.5 rounded-full text-[10px] font-bold bg-slate-100 text-slate-600"><i class="fa-solid fa-circle-minus mr-1"></i>Offen (${pct}%)</span>`;
                    barColor = 'bg-slate-300';
                }

                let diffDisplay = '';
                if (diff >= 0) {
                    diffDisplay = `<span class="text-emerald-600 font-semibold">+${diff} ${item.unit}</span>`;
                } else {
                    diffDisplay = `<span class="text-slate-400">${diff} ${item.unit}</span>`;
                }

                const tr = document.createElement('tr');
                tr.className = "hover:bg-slate-50/80 transition-colors";
                tr.innerHTML = `
                    <td class="py-3 px-4 font-semibold text-slate-800 flex items-center space-x-2.5">
                        <div class="w-7 h-7 rounded-lg bg-slate-100 text-slate-600 flex items-center justify-center text-xs">
                            <i class="fa-solid ${item.icon}"></i>
                        </div>
                        <span>${item.name}</span>
                    </td>
                    <td class="py-3 px-4 text-center font-medium text-slate-700 bg-slate-50/50">
                        ${targetVal} <span class="text-xs text-slate-400">${item.unit}</span>
                    </td>
                    <td class="py-3 px-4 text-center font-bold text-slate-900">
                        <input type="number" step="0.1" value="${item.consumed}" onchange="updateConsumedDirect('${item.id}', this.value)" class="w-20 px-2 py-1 text-center font-bold border border-slate-200 rounded-md focus:ring-2 focus:ring-emerald-500 focus:outline-none">
                        <span class="text-xs text-slate-400 font-normal">${item.unit}</span>
                    </td>
                    <td class="py-3 px-4">
                        <div class="space-y-1">
                            <div class="flex justify-between items-center text-xs">
                                ${statusBadge}
                            </div>
                            <div class="w-full bg-slate-100 h-2 rounded-full overflow-hidden">
                                <div class="${barColor} h-full transition-all duration-300" style="width: ${Math.min(pct, 100)}%"></div>
                            </div>
                        </div>
                    </td>
                    <td class="py-3 px-4 text-right text-xs">
                        ${diffDisplay}
                    </td>
                    <td class="py-3 px-4 text-center">
                        <div class="inline-flex rounded-md shadow-sm space-x-1" role="group">
                            <button onclick="adjustNutrientValue('${item.id}', 1)" class="px-2 py-1 text-xs font-bold text-slate-700 bg-slate-100 hover:bg-slate-200 rounded-l-md border border-slate-200">+1</button>
                            <button onclick="adjustNutrientValue('${item.id}', 10)" class="px-2 py-1 text-xs font-bold text-slate-700 bg-slate-100 hover:bg-slate-200 border border-slate-200">+10</button>
                            <button onclick="adjustNutrientValue('${item.id}', -1)" class="px-2 py-1 text-xs font-bold text-slate-700 bg-slate-100 hover:bg-slate-200 rounded-r-md border border-slate-200">-1</button>
                        </div>
                    </td>
                `;
                tbody.appendChild(tr);
            });
        }

        // Adjust nutrient value directly
        function adjustNutrientValue(id, delta) {
            const item = nutrientDatabase.find(n => n.id === id);
            if (item) {
                item.consumed = Math.max(0, parseFloat((item.consumed + delta).toFixed(2)));
                renderNutrientsTable();
                updateSummaryCards();
                saveToLocalStorage();
            }
        }

        function updateConsumedDirect(id, val) {
            const item = nutrientDatabase.find(n => n.id === id);
            if (item) {
                item.consumed = Math.max(0, parseFloat(parseFloat(val || 0).toFixed(2)));
                renderNutrientsTable();
                updateSummaryCards();
                saveToLocalStorage();
            }
        }

        // Summary Top Cards Update
        function updateSummaryCards() {
            const kcalItem = nutrientDatabase.find(n => n.id === 'kcal');
            const proteinItem = nutrientDatabase.find(n => n.id === 'protein');

            const kcalTarget = currentGender === 'm' ? kcalItem.rdaM : kcalItem.rdaW;
            const proteinTarget = currentGender === 'm' ? proteinItem.rdaM : proteinItem.rdaW;

            document.getElementById('summaryCalories').textContent = `${kcalItem.consumed} / ${kcalTarget} kcal`;
            document.getElementById('summaryCaloriesBar').style.width = `${Math.min((kcalItem.consumed / kcalTarget) * 100, 100)}%`;

            document.getElementById('summaryProtein').textContent = `${proteinItem.consumed} / ${proteinTarget} g`;
            document.getElementById('summaryProteinBar').style.width = `${Math.min((proteinItem.consumed / proteinTarget) * 100, 100)}%`;

            const vitItems = nutrientDatabase.filter(n => n.cat.startsWith('vit'));
            const vitMet = vitItems.filter(n => n.consumed >= (currentGender === 'm' ? n.rdaM : n.rdaW)).length;
            document.getElementById('summaryVitaminsCount').textContent = `${vitMet} / ${vitItems.length}`;
            document.getElementById('summaryVitaminsPct').textContent = `${Math.round((vitMet / vitItems.length) * 100)}% im Soll`;

            const minItems = nutrientDatabase.filter(n => n.cat === 'minerals');
            const minMet = minItems.filter(n => n.consumed >= (currentGender === 'm' ? n.rdaM : n.rdaW)).length;
            document.getElementById('summaryMineralsCount').textContent = `${minMet} / ${minItems.length}`;
            document.getElementById('summaryMineralsPct').textContent = `${Math.round((minMet / minItems.length) * 100)}% im Soll`;
        }

        // Preset Loader
        function loadPresetFood() {
            const key = document.getElementById('presetFoodSelect').value;
            if (!key || !foodPresets[key]) return;
            addPresetDirect(key);
        }

        function addPresetDirect(presetKey) {
            const preset = foodPresets[presetKey];
            if (!preset) return;

            let logDetails = [];
            for (const [nutId, val] of Object.entries(preset.nutrients)) {
                const item = nutrientDatabase.find(n => n.id === nutId);
                if (item) {
                    item.consumed = parseFloat((item.consumed + val).toFixed(2));
                    logDetails.push(`${item.name}: +${val}${item.unit}`);
                }
            }

            const now = new Date();
            const timeStr = now.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });

            foodLogs.unshift({
                id: Date.now(),
                time: timeStr,
                title: preset.name,
                details: logDetails.join(', ')
            });

            renderNutrientsTable();
            renderLogHistory();
            updateSummaryCards();
            saveToLocalStorage();
        }

        function addSingleNutrientLog() {
            const select = document.getElementById('logNutrientSelect');
            const amountInput = document.getElementById('logNutrientAmount');
            const nutId = select.value;
            const amount = parseFloat(amountInput.value);

            if (!amount || amount <= 0) return;

            const item = nutrientDatabase.find(n => n.id === nutId);
            if (item) {
                item.consumed = parseFloat((item.consumed + amount).toFixed(2));

                const now = new Date();
                const timeStr = now.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });

                foodLogs.unshift({
                    id: Date.now(),
                    time: timeStr,
                    title: `Einzelneingabe (${item.name})`,
                    details: `+${amount} ${item.unit}`
                });

                amountInput.value = '';
                renderNutrientsTable();
                renderLogHistory();
                updateSummaryCards();
                saveToLocalStorage();
            }
        }

        function removeLogEntry(logId) {
            foodLogs = foodLogs.filter(l => l.id !== logId);
            renderLogHistory();
            saveToLocalStorage();
        }

        function renderLogHistory() {
            const tbody = document.getElementById('logHistoryTableBody');
            tbody.innerHTML = '';

            document.getElementById('logCountBadge').textContent = `${foodLogs.length} Einträge`;

            if (foodLogs.length === 0) {
                tbody.innerHTML = `<tr><td colspan="4" class="py-8 text-center text-slate-400">Heute noch keine Verzehreinträge vorhanden.</td></tr>`;
                return;
            }

            foodLogs.forEach(log => {
                const tr = document.createElement('tr');
                tr.className = "hover:bg-slate-50";
                tr.innerHTML = `
                    <td class="py-2.5 px-3 text-slate-500 font-mono">${log.time}</td>
                    <td class="py-2.5 px-3 font-semibold text-slate-800">${log.title}</td>
                    <td class="py-2.5 px-3 text-slate-600">${log.details}</td>
                    <td class="py-2.5 px-3 text-right">
                        <button onclick="removeLogEntry(${log.id})" class="text-red-500 hover:text-red-700 text-xs font-semibold">
                            <i class="fa-solid fa-trash-can"></i>
                        </button>
                    </td>
                `;
                tbody.appendChild(tr);
            });
        }

        // EXCEL / CSV EXPORT AND IMPORT
        function generateCSVData() {
            let csv = "Nährstoff-ID;Nährstoff Name;Kategorie;Einheit;Empfohlene Tagesmenge (Männlich);Empfohlene Tagesmenge (Weiblich);Konsumiert Heute;Prozent Erreicht (%)\n";
            nutrientDatabase.forEach(item => {
                const targetVal = currentGender === 'm' ? item.rdaM : item.rdaW;
                const pct = Math.round((item.consumed / targetVal) * 100);
                csv += `${item.id};"${item.name}";${item.cat};${item.unit};${item.rdaM};${item.rdaW};${item.consumed};${pct}%\n`;
            });
            return csv;
        }

        function updateCsvPreview() {
            const area = document.getElementById('csvPreviewArea');
            if (area) {
                area.value = generateCSVData();
            }
        }

        function exportToExcelCSV() {
            const csvData = generateCSVData();
            const blob = new Blob(["\ufeff" + csvData], { type: 'text/csv;charset=utf-8;' });
            const url = URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = `NaehrstoffTracker_Export_${new Date().toISOString().slice(0, 10)}.csv`;
            document.body.appendChild(a);
            a.click();
            document.body.removeChild(a);
        }

        function importFromCSV(event) {
            const file = event.target.files[0];
            if (!file) return;

            const reader = new FileReader();
            reader.onload = function(e) {
                const text = e.target.result;
                const lines = text.split('\n');
                let count = 0;

                lines.forEach((line, index) => {
                    if (index === 0 || !line.trim()) return;
                    const parts = line.split(';');
                    if (parts.length >= 7) {
                        const nutId = parts[0].trim();
                        const consumedVal = parseFloat(parts[6].replace(',', '.'));

                        const item = nutrientDatabase.find(n => n.id === nutId);
                        if (item && !isNaN(consumedVal)) {
                            item.consumed = consumedVal;
                            count++;
                        }
                    }
                });

                alert(`${count} Nährstoffwerte erfolgreich aus CSV importiert!`);
                renderNutrientsTable();
                updateSummaryCards();
                updateCsvPreview();
                saveToLocalStorage();
            };
            reader.readAsText(file);
        }

        function resetTodayData() {
            if (confirm('Möchtest du die heute konsumierten Nährstoffe wirklich auf 0 zurücksetzen?')) {
                nutrientDatabase.forEach(item => item.consumed = 0);
                foodLogs = [];
                renderNutrientsTable();
                renderLogHistory();
                updateSummaryCards();
                updateCsvPreview();
                saveToLocalStorage();
            }
        }

        // Local Storage Persistence
        function saveToLocalStorage() {
            const data = {
                gender: currentGender,
                consumedMap: nutrientDatabase.map(n => ({ id: n.id, consumed: n.consumed })),
                foodLogs: foodLogs
            };
            localStorage.setItem('nutrientTrackerData', JSON.stringify(data));
        }

        function loadFromLocalStorage() {
            const saved = localStorage.getItem('nutrientTrackerData');
            if (!saved) return;
            try {
                const parsed = JSON.parse(saved);
                if (parsed.gender) setProfile(parsed.gender);
                if (parsed.consumedMap) {
                    parsed.consumedMap.forEach(savedItem => {
                        const item = nutrientDatabase.find(n => n.id === savedItem.id);
                        if (item) item.consumed = savedItem.consumed || 0;
                    });
                }
                if (parsed.foodLogs) foodLogs = parsed.foodLogs;
            } catch (e) {
                console.error("Error loading stored data", e);
            }
        }
    </script>
</body>
</html>
