import Foundation

@main
struct FreeFeatureChecks {
    static func main() {
        precondition(SearchModeResolver.enableEditing(mode: .off) == .enterEditing)
        precondition(SearchModeResolver.enableEditing(mode: .editing) == .placeCaretOnly)
        precondition(SearchModeResolver.startMode(startInSearch: true) == .editing)
        precondition(SearchModeResolver.toggle(mode: .editing) == .disable)
        precondition(SearchModeResolver.escape(mode: .editing, entry: .startedInSearch) == .closeSwitcher)
        precondition(SearchModeResolver.escape(mode: .editing, entry: .toggledMidSession) == .exitSearch)
        precondition(SearchModeResolver.routeKey(arrow: .down) == .cycleSelection(.down))
        precondition(SearchModeResolver.routeKey(hasMarkedText: true, arrow: .down) == .passToField)
        let search = SearchDiscoveryPolicy.Context(windowCount: 8, hasShortcut: true)
        precondition(search.isEligible(history: .init(hasSearched: false)))
        precondition(!search.isEligible(history: .init(hasSearched: true)))
        var history = SearchDiscoveryPolicy.History(hasSearched: false)
        for day in [0, 15, 35, 365, 3650] {
            let date = Date(timeIntervalSince1970: Double(day) * 86400)
            precondition(search.isEligible(history: history))
            precondition(history.canPresent(at: date))
        }
        history.recordSearch()
        precondition(!search.isEligible(history: history))
        print("Free search, search-on-release, key routing, discovery, and date checks passed")
    }
}
