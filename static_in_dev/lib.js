
// === html generation ================================================

let getDepartmentValue = (department) => {
    return department.name
}

let employeeTemplate = `{name} - {post} ({salary} rub) from {date}`
let employeeDismissedTemplate = `{name} - dismissed {post}`
let getEmployeeValue = (employee) => {
    let template = employee.department_id
        ? employeeTemplate
        : employeeDismissedTemplate
    let date = new Date(employee.date_employment).toLocaleDateString("ru")
    return template
        .replace("{name}", employee.name)
        .replace("{post}", employee.post_name)
        .replace("{salary}", employee.salary)
        .replace("{date}", date)
}


let liTemplate = `
    <li
            id="{id}"
            class="list-group-item nesting-{level} item-{type}"
            {onclick}
    >
        <div class="item-inner-text">{value}</div>
    </li>
`
let getLi = (obj, type) => {
    let value = type === "department" ? getDepartmentValue(obj) : getEmployeeValue(obj)
    let dots = "• ".repeat(obj.level)

    let onclick = type === "department"
        ? `onclick="expandThis('${obj.htmlId}')"`
        : ""

    return liTemplate
        .replace("{id}", obj.htmlId)
        .replace("{level}", obj.level)
        .replace("{type}", type)
        .replace("{onclick}", onclick)
        .replace("{value}", dots + value)
}

// ===
// === expand/collapse the tree =======================================

/*
* Adds the necessary fields for the deportment object (which is a tree
* node) and attaches it to the parent node.
* */
function attachDepartment(department, node, currentId) {
    let htmlId = "department" + department.id
    department.htmlId = htmlId
    $("#" + currentId).after(getLi(department, "department"))

    department.isExpanded = false
    department.child = []
    node.child.push(department)
    flatTree[htmlId] = department

    return htmlId
}

/*
* Adds the necessary fields for the employee object (tree leaf) and
* attaches it to the parent node.
* */
function attachEmployee(employee, node, currentId, type="employee") {
    let htmlId = "employee" + employee.id
    employee.htmlId = htmlId

    $("#" + currentId).after(getLi(employee, type))
    node.child.push(employee)

    return htmlId
}

/*
* Loads child elements for the target deportment.
* */
function getChild(node) {
    $.get("children/" + node.id + "/").done((data) => {
         let currentId = node.htmlId

        let departments = data.departments
        departments.forEach((department) => {
            currentId = attachDepartment(department, node, currentId)
        })

        let employees = data.employees
        employees.forEach((employee) => {
            currentId = attachEmployee(employee, node, currentId)
        })
    })
}

/*
* Recursively collapses all child elements.
* */
function collapseNode(node) {
    node.isExpanded = false
    if (node.child) {
        node.child.forEach((children) => {
            $("#" + children.htmlId).hide()
            collapseNode(children)
        })
    }
}

/*
* Loads (if not already present) and displays the child elements of the
* node (not recursively).
* */
function expandNode(node) {
    node.isExpanded = true

    if (!node.isChecked) {
        getChild(node)
        node.isChecked = true
    }

    node.child.forEach((children) => {
        $("#" + children.htmlId).show()
    })
}


function expandThis(htmlId) {
    let node = flatTree[htmlId]
    if (!node.child) { return }

    if (node.isExpanded) {
        collapseNode(node)
    } else {
        expandNode(node)
    }
}

// ===
// === tree initialization ============================================

let tree = {
    table: {
        // required fields for the node
        level: 0, // nesting level
        isExpanded: true, // node expanded/collapsed
        isChecked: true, // data has already been uploaded
        child: [], // daughter nodes and leaves; is the marker of the node (deportment)
    },
    dismissed: {
        level: 0,
        isExpanded: true,
        isChecked: true,
        child: [],
    },
}

//a set of tree nodes, but in flat form
// made to not implement a tree search, but to get elements from here
let flatTree = {
    table: tree.table,
    dismissed: tree.dismissed,
}

// Filling in the top level of departments and dismissed employees.
// It is similar to the `getChild` function with the difference that the
// deportments and employees are attached to two different nodes
$.get("children/").done(
    function (data) {
        let currentId, htmlId

        let departments = data.departments
        currentId = "table"
        departments.forEach((department) => {
            currentId = attachDepartment(department, tree.table, currentId)
        })

        let employees = data.employees
        currentId = "dismissed"
        employees.forEach((employee) => {
            currentId = attachEmployee(employee, tree.dismissed, currentId, "employee-dismiss")
        })
    }
)
