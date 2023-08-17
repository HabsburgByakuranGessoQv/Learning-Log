import copy


class Weighted_Gragh:
    def __init__(self, vertices):
        self.adjacent_table = {}
        for vertex in vertices:
            self.adjacent_table.update({vertex: {}})
        # print("Weighted Gragh has been created Successfully!!!!!")
        # print('self.adjacent_table', end=" -> \n")
        print(self.adjacent_table)

    def addNeighbor(self, source, terminal, weigh):
        neighbor_list = self.adjacent_table[source]
        neighbor_list.update({terminal: weigh})
        self.adjacent_table.update({source: neighbor_list})
        # print('Add a new Neighbor\nself.adjacent_table', end=" -> \n")
        print(self.adjacent_table)

    def maxCapacityAugmentation(self, source, terminal):
        print('--------------------------------------------------------------------------------------------------')
        self.f_table = {}
        self.r_table = copy.deepcopy(self.adjacent_table)

        path = self.findMaxBottleneckDFS(source, terminal, 0, {})
        while path:
            print(path)
            bottleneck = self.foundBottleneck(path, terminal)

            self.argumentFlow(bottleneck, path, terminal)

            path = self.findMaxBottleneckDFS(source, terminal, 0, {})

        return self.f_table

    def findMaxBottleneckDFS(self, source, terminal, level, level_table, max_bottleneck=1000):
        print((source, terminal, max_bottleneck))

        level += 1
        for end, weight in self.r_table[source].items():
            if weight > 0:
                if level not in level_table:
                    level_table[level] = {}
                if end not in level_table[level]:
                    level_table[level][end] = {}
                level_table[level][end] = {source: weight}
                if end == terminal:
                    return level_table
                if weight >= max_bottleneck:
                    return self.findMaxBottleneckDFS(end, terminal, level, level_table, max_bottleneck=max_bottleneck)
                elif weight < max_bottleneck:
                    return self.findMaxBottleneckDFS(end, terminal, level, level_table, max_bottleneck=weight)
            elif weight < 0:
                raise ("the value of weigh have some problem")

    def foundBottleneck(self, path, terminal):
        weight_list = []
        tmp_level = max(path.keys())
        # print('tmp_level', end=" ->")
        print(tmp_level)

        start = terminal
        while tmp_level > 0:
            for start, weight in path[tmp_level][start].items():
                pass
            tmp_level -= 1
            weight_list.append(weight)
        # print('Bottleneck of traffic -> {}'.format(min(weight_list)))
        return min(weight_list)

    def argumentFlow(self, bottleneck, path, terminal):
        tmp_level = max(path.keys())

        end = terminal
        print('path:\n', terminal, end="")
        while tmp_level > 0:
            for start, weight in path[tmp_level][end].items():
                pass
            print("->", start, weight, end="")
            if start not in self.f_table:
                self.f_table[start] = {}
            if end not in self.f_table[start]:
                self.f_table[start][end] = 0
            self.f_table[start][end] += bottleneck
            self.r_table[start][end] -= bottleneck
            tmp_level -= 1
            end = start


if __name__ == '__main__':
    gragh = Weighted_Gragh(['a', 'b', 'c', 'd'])
    gragh.addNeighbor('a', 'b', 1000000)
    gragh.addNeighbor('b', 'd', 1000000)
    gragh.addNeighbor('c', 'd', 1000000)
    gragh.addNeighbor('a', 'c', 1000000)
    gragh.addNeighbor('b', 'c', 1)

    gragh.maxCapacityAugmentation('a', 'd')










































print('max: 2000000')
