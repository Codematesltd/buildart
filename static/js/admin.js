function openModal(type) {
    const modal = document.getElementById(`${type}-modal`);
    modal.classList.remove('hidden');
}

function closeModal(type) {
    const modal = document.getElementById(`${type}-modal`);
    modal.classList.add('hidden');
}

function renderProjects(projects) {
    const container = document.getElementById('projects-table');
    container.innerHTML = `
        <table class="min-w-full divide-y divide-gray-200">
            <thead>
                <tr>
                    <th class="px-6 py-3 bg-gray-50 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Name</th>
                    <th class="px-6 py-3 bg-gray-50 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Description</th>
                    <th class="px-6 py-3 bg-gray-50 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Actions</th>
                </tr>
            </thead>
            <tbody class="bg-white divide-y divide-gray-200">
                ${projects.map(project => `
                    <tr>
                        <td class="px-6 py-4 whitespace-nowrap">${project.name}</td>
                        <td class="px-6 py-4">${project.description}</td>
                        <td class="px-6 py-4 whitespace-nowrap">
                            <button onclick="editProject(${project.id})" class="text-indigo-600 hover:text-indigo-900">Edit</button>
                            <button onclick="deleteProject(${project.id})" class="text-red-600 hover:text-red-900 ml-4">Delete</button>
                        </td>
                    </tr>
                `).join('')}
            </tbody>
        </table>
    `;
}

function renderAwards(awards) {
    const container = document.getElementById('awards-table');
    container.innerHTML = `
        <table class="min-w-full divide-y divide-gray-200">
            <thead>
                <tr>
                    <th class="px-6 py-3 bg-gray-50 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Year</th>
                    <th class="px-6 py-3 bg-gray-50 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Award</th>
                    <th class="px-6 py-3 bg-gray-50 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Project</th>
                    <th class="px-6 py-3 bg-gray-50 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Actions</th>
                </tr>
            </thead>
            <tbody class="bg-white divide-y divide-gray-200">
                ${awards.map(award => `
                    <tr>
                        <td class="px-6 py-4 whitespace-nowrap">${award.year}</td>
                        <td class="px-6 py-4">${award.award_name}</td>
                        <td class="px-6 py-4">${award.project}</td>
                        <td class="px-6 py-4 whitespace-nowrap">
                            <button onclick="editAward(${award.id})" class="text-indigo-600 hover:text-indigo-900">Edit</button>
                            <button onclick="deleteAward(${award.id})" class="text-red-600 hover:text-red-900 ml-4">Delete</button>
                        </td>
                    </tr>
                `).join('')}
            </tbody>
        </table>
    `;
}
